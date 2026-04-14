from llama_index.llms.ollama import Ollama

llm = Ollama(model="llama3.1:8b", request_timeout=120.0)
response = llm.complete("What causes handover failures in 5G RAN networks?")
print(response)