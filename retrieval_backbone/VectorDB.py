from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
import os

class VectorDB:
    """
    FAISS-based vector database for document retrieval using sentence embeddings.
    Uses SentenceTransformer for storing document chunks and similarity searching.
    """
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # initialize the embedding model
        self.model = SentenceTransformer(model_name)
        self.index = None   # FAISS index
        self.documents = [] # keep track of text + metadata
        self.dim = None     # dimension of embeddings

    # add documents and build index
    def add_documents(self, documents):
        if not documents:
            print("No documents to add.")
            return
        
        # extract text from the docs
        texts = [doc["text"] for doc in documents]
        # embed the texts using the model
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        
        # step 1 --> build index
        if self.index is None:
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dim)  # cosine similarity (assumes normalized embeddings)
            self.dim = dim
            print(f"New FAISS index created with dim={dim}")
        
        # add embeddings to the index
        self.index.add(np.array(embeddings).astype("float32"))
        # store the documents with metadata
        self.documents.extend(documents)
        print(f"Added {len(documents)} documents. Total vectors in index: {self.index.ntotal}")

    # step 2 --> save index and docs
    def save(self, save_dir="faiss_store"):
        if self.index is None:
            print("No index to save.")
            return
        
        os.makedirs(save_dir, exist_ok=True)
        faiss.write_index(self.index, os.path.join(save_dir, "index.bin"))
        
        with open(os.path.join(save_dir, "documents.pkl"), "wb") as f:
            pickle.dump(self.documents, f)
        print(f"Index and documents saved to {save_dir}")

    # step 3 --> load index and docs for searching
    @classmethod
    def load(cls, save_dir="faiss_store", model_name="all-MiniLM-L6-v2"):
        db = cls(model_name=model_name)
        db.index = faiss.read_index(os.path.join(save_dir, "index.bin"))
        
        with open(os.path.join(save_dir, "documents.pkl"), "rb") as f:
            db.documents = pickle.load(f)
            
        db.dim = db.index.d
        print(f"Index and documents loaded from {save_dir}")
        print(f"{len(db.documents)} documents in index with {db.index.ntotal} vectors.")
        return db

    # step 4 --> search on the index
    def search(self, query, k=2, threshold=0.3):
        if self.index is None:
            print("Index not loaded.")
            return []
        
        # embed the query
        query_embeddings = self.model.encode([query], normalize_embeddings=True)
        # search for top 2 matches (will increase when real docs are added)
        D, I = self.index.search(np.array(query_embeddings).astype("float32"), k=k)

        results = []
        
        print(f"\nQuery: {query}\n")
        
        for idx, score in zip(I[0], D[0]):
            if score < threshold:
                print(f"[Score {score:.4f}] No relevant documents found.\n")
                continue
            
            doc = self.documents[idx]
            result = {
                "score": score,
                "text": doc["text"],
                "metadata": doc["metadata"]
            }
            
            results.append(result)
            
            meta = doc.get("metadata", {})
            src = meta.get("source_file", "unknown source")
            page = meta.get("source_page", "unknown page")
            print(f"[Score {score:.4f}] From {src}, page {page}")
            print(f"   {doc['text'][:200]}\n")
            
            # print(f"[Score {score:.4f}] {doc['metadata']}")
            # print(f"   {doc['text']}\n")
            
            if not results:
                print("No relevant documents found.\n")
                
        return results
    
    def clear(self):
        self.index = None
        self.documents = []
        self.dim = None
        print("Cleared the vector database.")