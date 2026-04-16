# src/ingest.py
import pandas as pd
import os
from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import chromadb

# ── settings ───────────────────────────────────────────────────────────────────

Settings.llm = Ollama(model="llama3.2:3b", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

CHROMA_PATH = "chroma_db"
PROCESSED_CSV = "data/processed/faulted_dataset.csv"
INCIDENT_REPORTS_DIR = "data/incident_reports"

# ── log rows → text chunks ─────────────────────────────────────────────────────

def kpi_row_to_text(row):
    """Convert a single KPI row into a readable text description."""
    fault_info = ""
    if row["fault_label"] == 1:
        fault_info = f"FAULT DETECTED — type: {row['fault_type']}. "

    return (
        f"{fault_info}"
        f"Timestamp: {row['Timestamp']}. "
        f"Cell ID: {row['CellID']}. "
        f"Network: {row['NetworkMode']}. "
        f"App: {row['source_app']} ({row['source_mobility']}). "
        f"RSRP: {row['RSRP']} dBm. "
        f"RSRQ: {row['RSRQ']} dB. "
        f"SNR: {row['SNR']} dB. "
        f"DL bitrate: {row['DL_bitrate']} kbps. "
        f"UL bitrate: {row['UL_bitrate']} kbps. "
        f"Speed: {row['Speed']} km/h. "
        f"Source file: {row['source_file']}."
    )

def load_kpi_documents(csv_path, max_faulted=500, max_normal=200):
    """Load a balanced sample of KPI rows as Documents."""
    df = pd.read_csv(csv_path, low_memory=False)

    faulted = df[df["fault_label"] == 1].sample(
        min(max_faulted, len(df[df["fault_label"] == 1])), random_state=42
    )
    normal = df[df["fault_label"] == 0].sample(
        min(max_normal, len(df[df["fault_label"] == 0])), random_state=42
    )
    sampled = pd.concat([faulted, normal]).reset_index(drop=True)

    docs = []
    for _, row in sampled.iterrows():
        text = kpi_row_to_text(row)
        doc = Document(
            text=text,
            metadata={
                "source": "kpi_log",
                "fault_type": str(row["fault_type"]),
                "fault_label": int(row["fault_label"]),
                "cell_id": str(row["CellID"]),
                "app": str(row["source_app"]),
                "mobility": str(row["source_mobility"]),
            }
        )
        docs.append(doc)

    print(f"Loaded {len(docs)} KPI documents ({len(faulted)} faulted, {len(normal)} normal)")
    return docs

def load_incident_documents(reports_dir):
    """Load all incident report markdown files as Documents."""
    docs = []
    for fname in os.listdir(reports_dir):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(reports_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        fault_type = "general"
        if "rsrp_drop" in fname:
            fault_type = "rsrp_drop"
        elif "handover" in fname:
            fault_type = "handover_failure"
        elif "throughput" in fname:
            fault_type = "throughput_collapse"
        doc = Document(
            text=content,
            metadata={
                "source": "incident_report",
                "fault_type": fault_type,
                "filename": fname,
            }
        )
        docs.append(doc)
    print(f"Loaded {len(docs)} incident report documents")
    return docs

# ── build index ────────────────────────────────────────────────────────────────

def build_index():
    os.makedirs(CHROMA_PATH, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    # separate collections for logs vs docs
    kpi_collection = chroma_client.get_or_create_collection("kpi_logs")
    ir_collection  = chroma_client.get_or_create_collection("incident_reports")

    kpi_docs = load_kpi_documents(PROCESSED_CSV)
    ir_docs  = load_incident_documents(INCIDENT_REPORTS_DIR)

    print("\nIndexing KPI logs...")
    kpi_store   = ChromaVectorStore(chroma_collection=kpi_collection)
    kpi_context = StorageContext.from_defaults(vector_store=kpi_store)
    kpi_index   = VectorStoreIndex.from_documents(kpi_docs, storage_context=kpi_context, show_progress=True)

    print("\nIndexing incident reports...")
    ir_store    = ChromaVectorStore(chroma_collection=ir_collection)
    ir_context  = StorageContext.from_defaults(vector_store=ir_store)
    ir_index    = VectorStoreIndex.from_documents(ir_docs, storage_context=ir_context, show_progress=True)

    print("\nIndexing complete. Collections saved to chroma_db/")
    return kpi_index, ir_index

if __name__ == "__main__":
    build_index()