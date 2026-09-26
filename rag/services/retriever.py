import faiss
import pickle
import numpy as np

from .embeddings import model

INDEX_PATH = "vector_db/index.faiss"
CHUNKS_PATH = "vector_db/chunks.pkl"

def retrieve_chunks(question , top_k=3):
    index=faiss.read_index(INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    
    question_embedding = model.encode([question])
    question_embedding = np.array(question_embedding).astype('float32')
    
    distances, indices = index.search(
        question_embedding,
        top_k
    )
    
    result=[]
    
    for index in indices[0]:
        if index<len(chunks):
            result.append(chunks[index])
            
    return result