import os
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

METADATA_FILE = os.path.join(os.path.dirname(__file__), 'metadata_index.txt')
FAISS_INDEX_FILE = os.path.join(os.path.dirname(__file__), 'faiss_metadata.index')
EMBEDDINGS_FILE = os.path.join(os.path.dirname(__file__), 'metadata_embeddings.npy')
CHUNKS_FILE = os.path.join(os.path.dirname(__file__), 'metadata_chunks.txt')

# Use a lightweight, open-source embedding model
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'


def load_metadata_chunks(metadata_file=METADATA_FILE):
    with open(metadata_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Split on separator lines
    chunks = [chunk.strip() for chunk in content.split('-' * 40) if chunk.strip()]
    return chunks


def build_faiss_index(chunks, model_name=EMBEDDING_MODEL, index_file=FAISS_INDEX_FILE, emb_file=EMBEDDINGS_FILE, chunks_file=CHUNKS_FILE):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, index_file)
    np.save(emb_file, embeddings)
    with open(chunks_file, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(chunk + '\n' + '-'*40 + '\n')
    print(f"FAISS index built and saved to {index_file}")


def search_metadata(query, top_k=3, model_name=EMBEDDING_MODEL, index_file=FAISS_INDEX_FILE, emb_file=EMBEDDINGS_FILE, chunks_file=CHUNKS_FILE):
    model = SentenceTransformer(model_name)
    index = faiss.read_index(index_file)
    embeddings = np.load(emb_file)
    with open(chunks_file, 'r', encoding='utf-8') as f:
        chunks = [chunk.strip() for chunk in f.read().split('-' * 40) if chunk.strip()]
    query_emb = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_emb, top_k)
    results = [chunks[i] for i in I[0]]
    return results


def main():
    chunks = load_metadata_chunks()
    build_faiss_index(chunks)
    print("Indexing complete. You can now use search_metadata(query) to retrieve relevant metadata.")


if __name__ == "__main__":
    main()
