# app.py
import gradio as gr
import pandas as pd
import chromadb
from llama_index.core import VectorStoreIndex, Settings, QueryBundle
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate

# ── settings ───────────────────────────────────────────────────────────────────

Settings.llm = Ollama(model="llama3.2:3b", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

CHROMA_PATH = "chroma_db"
PROCESSED_CSV = "data/processed/faulted_dataset.csv"

RCA_PROMPT = PromptTemplate(
    "You are an expert telecom network engineer specializing in 5G RAN "
    "root cause analysis. You work for a network operations center (NOC) "
    "and your job is to diagnose faults from KPI logs and incident reports.\n\n"
    "Use ONLY the context below to answer. Be specific — name the exact fault type, "
    "cite the KPI values that indicate the fault, and recommend concrete resolution steps.\n"
    "If the context does not contain enough information, say so clearly.\n\n"
    "Context:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n\n"
    "Question: {query_str}\n\n"
    "Answer (structure your response as: "
    "1) Fault type  2) Evidence from KPIs  3) Root cause  4) Resolution steps):"
)

# ── load indexes ───────────────────────────────────────────────────────────────

print("Loading indexes...")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
kpi_store     = ChromaVectorStore(chroma_collection=chroma_client.get_collection("kpi_logs"))
ir_store      = ChromaVectorStore(chroma_collection=chroma_client.get_collection("incident_reports"))
kpi_index     = VectorStoreIndex.from_vector_store(kpi_store)
ir_index      = VectorStoreIndex.from_vector_store(ir_store)
kpi_retriever = VectorIndexRetriever(index=kpi_index, similarity_top_k=3)
ir_engine     = ir_index.as_query_engine(
    similarity_top_k=3,
    text_qa_template=RCA_PROMPT,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.3)],
)
print("Indexes loaded.")

# ── load KPI data for chart ────────────────────────────────────────────────────

print("Loading KPI data...")
df_kpi = pd.read_csv(PROCESSED_CSV, low_memory=False)
df_kpi["RSRP"]       = pd.to_numeric(df_kpi["RSRP"], errors="coerce")
df_kpi["DL_bitrate"] = pd.to_numeric(df_kpi["DL_bitrate"], errors="coerce")
df_kpi["row_index"]  = range(len(df_kpi))
print("KPI data loaded.")

# ── chart builder ──────────────────────────────────────────────────────────────

def build_chart(fault_type_filter):
    if fault_type_filter == "All faults":
        subset = df_kpi[df_kpi["fault_label"] == 1].copy()
    else:
        subset = df_kpi[df_kpi["fault_type"] == fault_type_filter].copy()

    normal_sample = df_kpi[df_kpi["fault_label"] == 0].sample(
        min(300, len(df_kpi[df_kpi["fault_label"] == 0])), random_state=42
    )
    plot_df = pd.concat([normal_sample, subset]).sort_values("row_index")

    return pd.DataFrame({
        "Index":           plot_df["row_index"].values,
        "RSRP (dBm)":     plot_df["RSRP"].values,
        "DL bitrate":     plot_df["DL_bitrate"].values,
        "Fault":          plot_df["fault_type"].values,
    })

# ── query function ─────────────────────────────────────────────────────────────

def run_query(question, history):
    if not question.strip():
        return history, "", ""

    kpi_nodes = kpi_retriever.retrieve(QueryBundle(question))
    kpi_evidence = ""
    for i, node in enumerate(kpi_nodes):
        score = round(node.score, 3) if node.score else "N/A"
        kpi_evidence += f"**[{i+1}] similarity={score}**\n\n{node.text}\n\n---\n\n"

    ir_retriever_local = VectorIndexRetriever(index=ir_index, similarity_top_k=3)
    ir_nodes = ir_retriever_local.retrieve(QueryBundle(question))
    ir_evidence = ""
    for i, node in enumerate(ir_nodes):
        score = round(node.score, 3) if node.score else "N/A"
        fname = node.metadata.get("filename", "unknown")
        ir_evidence += f"**[{i+1}] {fname}** (similarity={score})\n\n{node.text[:300]}...\n\n---\n\n"

    sources_text = "### KPI Log Evidence\n\n" + kpi_evidence + \
                   "### Incident Reports Retrieved\n\n" + ir_evidence

    response = ir_engine.query(question)
    answer   = str(response)

    history = history or []
    history.append({"role": "user",      "content": question})
    history.append({"role": "assistant", "content": answer})
    return history, sources_text, ""

# ── preset loader ──────────────────────────────────────────────────────────────

PRESETS = [
    "Why is cell 12 experiencing throughput collapse despite good signal?",
    "What is causing handover failures in the driving scenario?",
    "Why has RSRP dropped below -110 dBm on multiple cells?",
    "What should I check if DL bitrate collapses but RSRP looks normal?",
]

# ── UI ─────────────────────────────────────────────────────────────────────────

with gr.Blocks(title="5G RAN Root Cause Analysis") as demo:

    gr.Markdown("""
    # 5G RAN Root Cause Analysis Assistant
    **RAG-powered NOC assistant** — ask questions about your 5G KPI logs and get
    sourced, structured root cause analysis backed by real incident reports.
    """)

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### Ask a fault question")
            chatbot = gr.Chatbot(height=400, label="RCA Diagnosis")
            question_box = gr.Textbox(
                placeholder="e.g. Why is cell 12 experiencing handover failures?",
                label="Your question",
                lines=2,
            )
            with gr.Row():
                submit_btn = gr.Button("Diagnose", variant="primary")
                clear_btn  = gr.Button("Clear")

            gr.Markdown("### Preset example queries")
            for preset in PRESETS:
                btn = gr.Button(preset, size="sm")
                btn.click(fn=lambda p=preset: p, outputs=question_box)

        with gr.Column(scale=1):
            gr.Markdown("### Retrieved sources")
            sources_box = gr.Markdown(
                value="_Sources will appear here after a query._"
            )

    gr.Markdown("### KPI overview — RSRP & throughput with fault markers")
    fault_filter = gr.Radio(
        choices=["All faults", "rsrp_drop", "handover_failure", "throughput_collapse"],
        value="All faults",
        label="Filter fault type",
    )
    kpi_chart = gr.LinePlot(
        value=build_chart("All faults"),
        x="Index",
        y="RSRP (dBm)",
        color="Fault",
        title="RSRP over dataset (colored by fault type)",
        height=300,
    )

    fault_filter.change(fn=build_chart, inputs=fault_filter, outputs=kpi_chart)

    submit_btn.click(
        fn=run_query,
        inputs=[question_box, chatbot],
        outputs=[chatbot, sources_box, question_box],
    )
    question_box.submit(
        fn=run_query,
        inputs=[question_box, chatbot],
        outputs=[chatbot, sources_box, question_box],
    )
    clear_btn.click(
        fn=lambda: ([], "_Sources will appear here after a query._", ""),
        outputs=[chatbot, sources_box, question_box],
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())