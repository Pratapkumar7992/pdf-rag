import os 
import pickle
import faiss
import numpy as np

VECTOR_DB_PATH = "vector_db"
INDEX_PATH = os.path.join(VECTOR_DB_PATH, "index.faiss")
CHUNKS_PATH = os.path.join(VECTOR_DB_PATH, "chunks.pkl")

def create_vector_store(embedding,chunks):
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    embeddings = np.array(embedding).astype("float32")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as file:
        pickle.dump(chunks, file)
        
    return index
    