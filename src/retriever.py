import faiss
import pickle
import numpy as np

def build_faiss_index(embeddings, chunks, index_path):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    with open(index_path, "wb") as f:
        pickle.dump((index, chunks), f)

def load_faiss_index(index_path):
    with open(index_path, "rb") as f:
        return pickle.load(f)

def search_index(query_embedding, index, chunks, top_k=5):
    query_embedding = np.array([query_embedding])
    distances, indices = index.search(query_embedding, top_k)
    return [chunks[i] for i in indices[0]]