from sentence_transformers import  SentenceTransformer
import numpy as np
import faiss
import pickle
import os

mock_documents = [
    {"text": "How to descale Coffee Machine Model X step by step.", 
     "metadata": {"source": "manual1.pdf", "page": 2}},
    {"text": "Warranty policy covers machine parts for 2 years.", 
     "metadata": {"source": "manual2.pdf", "page": 5}},
    {"text": "To reset the coffee machine, hold the power button for 10 seconds.", 
     "metadata": {"source": "manual3.pdf", "page": 8}},
]


model = SentenceTransformer("all-MiniLM-L6-v2")  # would be replaced with Ollama

texts = [doc["text"] for doc in mock_documents]
embeddings = model.encode(texts, normalize_embeddings=True)  

dim = embeddings.shape[1]
print(f"Embedding dimension: {dim}")

index = faiss.IndexFlatIP(dim)  # using cosine similarity (assumes embeddings are normalized)
index.add(np.array(embeddings).astype("float32"))
print(f"FAISS index built with {index.ntotal} vectors")
print("Index is trained:", index.is_trained)
print("Index dimension:", index.d)
print("Index: ", index)

# Viewing the first 3 embeddings, will show first 10 numbers of each
xb = index.reconstruct_n(0, min(3, index.ntotal))  
print("First vector:", xb[0][:10])  # show first 10 numbers


# Save index and documents
def save_index(index, documents, save_dir="faiss_store"):
    os.makedirs(save_dir, exist_ok=True)
    
    # Index docs stored as binary files
    faiss.write_index(index, os.path.join(save_dir, "index.bin"))
    with open(os.path.join(save_dir, "documents.pkl"), "wb") as f:
        pickle.dump(documents, f)
    print("Index and documents saved.")
    
# Load index and documents
def load_index(save_dir="faiss_store"):
    index = faiss.read_index(os.path.join(save_dir, "index.bin"))
    with open(os.path.join(save_dir, "documents.pkl"), "rb") as f:
        documents = pickle.load(f)
    print("Index and documents loaded.")
    return index, documents

save_index(index, mock_documents)

# Sample search on loaded index
def search(query, index, docs, k=2, threshold=0.3):
    query_embeddings = model.encode([query], normalize_embeddings=True)
    D, I = index.search(np.array(query_embeddings).astype("float32"), k=k)

    print(f"\nQuery: {query}\n")
    for idx, score in zip(I[0], D[0]):
        if score < threshold:
            print(f"[Score {score:.4f}] No relevant documents found above threshold {threshold}.\n")
            continue
        
        doc = docs[idx]
        print(f"[Score {score:.4f}] {doc['metadata']}")
        print(f"   {doc['text']}\n")
        
    
index, documents = load_index()
search("How to reset the coffee machine?", index, documents, k=2)
search("What is the warranty period?", index, documents, k=2)
search("Steps to descale the coffee maker?", index, documents, k=2)
search("What month is it?", index, documents, k=2)  # Should return irrelevant results
