# src/query.py
import chromadb
from llama_index.core import VectorStoreIndex, Settings, QueryBundle
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate

# ── settings ───────────────────────────────────────────────────────────────────

Settings.llm = Ollama(model="llama3.2:3b", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

CHROMA_PATH = "chroma_db"

# ── RCA prompt ─────────────────────────────────────────────────────────────────

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

def load_indexes():
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    kpi_collection = chroma_client.get_collection("kpi_logs")
    ir_collection  = chroma_client.get_collection("incident_reports")

    kpi_store = ChromaVectorStore(chroma_collection=kpi_collection)
    ir_store  = ChromaVectorStore(chroma_collection=ir_collection)

    kpi_index = VectorStoreIndex.from_vector_store(kpi_store)
    ir_index  = VectorStoreIndex.from_vector_store(ir_store)

    return kpi_index, ir_index

# ── query engine ───────────────────────────────────────────────────────────────

def build_query_engine(kpi_index, ir_index, top_k=3):
    kpi_retriever = VectorIndexRetriever(index=kpi_index, similarity_top_k=top_k)
    ir_retriever  = VectorIndexRetriever(index=ir_index,  similarity_top_k=top_k)

    ir_engine = ir_index.as_query_engine(
        similarity_top_k=top_k,
        text_qa_template=RCA_PROMPT,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.3)],
    )
    return kpi_retriever, ir_retriever, ir_engine

# ── main query function ────────────────────────────────────────────────────────

def query_rca(question: str, kpi_retriever, ir_retriever, ir_engine):
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")

    # retrieve from both collections
    kpi_nodes = kpi_retriever.retrieve(QueryBundle(question))
    ir_nodes  = ir_retriever.retrieve(QueryBundle(question))

    # show retrieved KPI evidence
    print(f"\n--- Retrieved KPI log evidence ({len(kpi_nodes)} chunks) ---")
    for i, node in enumerate(kpi_nodes):
        score = round(node.score, 3) if node.score else "N/A"
        print(f"[{i+1}] score={score} | {node.text[:120]}...")

    # show retrieved incident reports
    print(f"\n--- Retrieved incident reports ({len(ir_nodes)} chunks) ---")
    for i, node in enumerate(ir_nodes):
        score = round(node.score, 3) if node.score else "N/A"
        fname = node.metadata.get("filename", "unknown")
        print(f"[{i+1}] score={score} | {fname}")

    # generate answer
    print(f"\n--- RCA Answer ---")
    response = ir_engine.query(question)
    print(response)

    return response

# ── test ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    kpi_retriever, ir_retriever, ir_engine = build_query_engine(*load_indexes())

    test_questions = [
        "Why is cell 12 experiencing handover failures?",
        "What is causing the throughput collapse despite good RSRP?",
        "Why has RSRP dropped below -110 dBm on multiple cells?",
    ]

    for q in test_questions:
        query_rca(q, kpi_retriever, ir_retriever, ir_engine)
        print("\n")