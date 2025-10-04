from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
import os

class VectorDB:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # initialize the embedding model
        self.model = SentenceTransformer(model_name)
        self.index = None   # FAISS index
        self.documents = [] # keep track of text + metadata
        self.dim = None     # dimension of embeddings

    # add documents and build index
    def add_documents(self, documents):
        # extract text from the docs
        texts = [doc["text"] for doc in documents]
        # embed the texts using the model
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        
        # step 1 --> build index
        if self.index is None:
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dim)  # cosine similarity (assumes normalized embeddings)
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
            results.append((score, doc))
            print(f"[Score {score:.4f}] {doc['metadata']}")
            print(f"   {doc['text']}\n")
        return results


# Example with mock documents 
mock_documents = [
    {"text": "How to descale Coffee Machine Model X step by step.", 
     "metadata": {"source": "manual1.pdf", "page": 2}},
    {"text": "Warranty policy covers machine parts for 2 years.", 
     "metadata": {"source": "manual2.pdf", "page": 5}},
    {"text": "To reset the coffee machine, hold the power button for 10 seconds.", 
     "metadata": {"source": "manual3.pdf", "page": 8}},
    {"text": "The coffee machine has a water filter that needs to be replaced every 3 months.", 
     "metadata": {"source": "manual4.pdf", "page": 3}},
    {"text": "For optimal performance, clean the coffee machine's brew group weekly.", 
     "metadata": {"source": "manual5.pdf", "page": 4}},
    {"text": "Store managers should perform daily inventory checks before 10 AM.", 
     "metadata": {"source": "store_policy.pdf", "page": 1}},
    {"text": "Employees must wear their ID badges at all times while on store premises.", 
     "metadata": {"source": "store_policy.pdf", "page": 2}},
    {"text": "All cash transactions must be recorded in the POS system immediately.", 
     "metadata": {"source": "store_policy.pdf", "page": 3}},
]

# create DB and add documents
db = VectorDB()
db.add_documents(mock_documents)
print(f"FAISS index built with {db.index.ntotal} vectors. \n")
print("Index is trained:", db.index.is_trained)
print("Index dimension:", db.index.d)
print("Index: ", db.index)
xb = db.index.reconstruct_n(0, min(3, db.index.ntotal))  
print("\n Vector 1:", xb[0][:10]) 

# save the DB
db.save()

# reload the DB
db_loaded = VectorDB.load()

# run some searches
db_loaded.search("How to reset the coffee machine?", k=2)
db_loaded.search("What is the warranty period?", k=2)
db_loaded.search("Steps to descale the coffee maker?", k=2)
db_loaded.search("What month is it?", k=2)  # should return nothing
db_loaded.search("How often to change water filter?", k=2)
db_loaded.search("Employee ID badge policy?", k=2)
db_loaded.search("Cash transaction procedures?", k=2)