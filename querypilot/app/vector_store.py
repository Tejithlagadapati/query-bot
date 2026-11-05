import chromadb

from app.chunking import chunk_documents
from app.config import CHROMA_DIR, COLLECTION_NAME
from app.document_loader import load_all_documents
from app.embeddings import embed


def get_collection():
    """Open (or create) the persistent Chroma collection."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},  # cosine distance for search
    )


def build_index():
    """Chunk every document, embed each chunk, and store everything in Chroma."""
    collection = get_collection()

    chunks = chunk_documents(load_all_documents())

    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    embeddings = [embed(chunk["text"]) for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            # Chroma rejects None, so -1 means "this file has no pages"
            "page": -1 if chunk["page"] is None else chunk["page"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"Indexed {len(chunks)} chunks. Collection now holds {collection.count()}.")


if __name__ == "__main__":
    build_index()