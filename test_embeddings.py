# test_embeddings.py
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")

test_texts = [
    "Handover failure detected on cell 7, RSRP dropped below -110 dBm",
    "High interference causing SINR degradation in sector 3",
]

for text in test_texts:
    embedding = embed_model.get_text_embedding(text)
    print(f"Text: {text[:50]}...")
    print(f"Embedding dim: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}\n")