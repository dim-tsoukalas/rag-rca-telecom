# test_full_stack.py
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb

# configure global settings
Settings.llm = Ollama(model="llama3.1:8b", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

# dummy telecom documents
docs = [
    Document(text="Cell 7 experienced a handover failure at 14:32 UTC. RSRP dropped to -115 dBm, below the -110 dBm threshold. Root cause: pilot pollution from overlapping sector 3."),
    Document(text="Throughput collapse observed on cell 12. PRB utilization hit 98% for 8 consecutive minutes. Root cause: traffic surge without load balancing trigger."),
    Document(text="SINR degradation on sector 4 between 09:00-09:45 UTC. Interference from adjacent cell on same PCI. Root cause: PCI collision after recent site addition."),
]

# set up chroma
chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("telecom_test")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# index documents
print("Indexing documents...")
index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)

# query
query_engine = index.as_query_engine()
print("Querying...\n")
response = query_engine.query("Why did cell 7 have a handover failure?")
print(f"Answer: {response}")