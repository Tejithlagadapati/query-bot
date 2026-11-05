from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_OVERLAP, CHUNK_SIZE
from app.document_loader import load_all_documents
import re

# i have to remove this later, just for tesing purpose only.
def chunk_fixed(text, size, overlap):
    """Baseline: cut every `size` characters, with `overlap` shared between neighbours."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")

    step = size - overlap
    chunks = []
    for start in range(0, len(text), step):
        chunks.append(text[start:start + size])
        if start + size >= len(text):
            break
    return chunks

def clean_text(text):
    """Tidy extracted text so paragraph breaks are plain blank lines."""
    text = re.sub(r"[ \t]+\n", "\n", text)  # drop spaces/tabs before a newline
    text = re.sub(r"\n{3,}", "\n\n", text)  # 3+ newlines become one blank line
    return text.strip()                     # trim the start and end

def chunk_recursive(text, size, overlap):
    """LangChain splitter: prefers paragraph breaks, then lines, then spaces."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
    )
    return splitter.split_text(text)

def chunk_documents(documents, chunker=chunk_recursive, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Turn loaded documents into chunk dicts ready for the vector database.

    Each dict has: id, source, page, chunk_index, text.
    """
    all_chunks = []

    for doc in documents:
        text = clean_text(doc["text"])
        pieces = chunker(text, size, overlap)
        page_label = "-" if doc["page"] is None else doc["page"]

        for index, piece in enumerate(pieces):
            if not piece.strip():
                continue  # skip empty chunks
            all_chunks.append({
                "id": f"{doc['source']}::p{page_label}::c{index}",
                "source": doc["source"],
                "page": doc["page"],
                "chunk_index": index,
                "text": piece,
            })

    return all_chunks
    
def rule_is_intact(chunks):
    """True if at least one chunk holds the whole software approval rule."""
    return any("10,000" in chunk and "approval" in chunk for chunk in chunks)

if __name__ == "__main__":
    documents = load_all_documents()

    # Part 1: chunker comparison (for docs/experiments.md)
    print("=== Chunker comparison ===")
    for doc in documents:
        text = clean_text(doc["text"])
        fixed = chunk_fixed(text, CHUNK_SIZE, CHUNK_OVERLAP)
        recursive = chunk_recursive(text, CHUNK_SIZE, CHUNK_OVERLAP)
        print(f"\n{doc['source']} (page {doc['page']})")
        print(f"  fixed:     {len(fixed)} chunks, lengths {[len(c) for c in fixed]}")
        print(f"  recursive: {len(recursive)} chunks, lengths {[len(c) for c in recursive]}")
        if "₹10,000" in text:
            print(f"  rule intact? fixed={rule_is_intact(fixed)} recursive={rule_is_intact(recursive)}")

    # Part 2: metadata chunks (what the vector database will receive)
    print("\n=== Chunks with metadata ===")
    chunks = chunk_documents(documents)
    print("Total chunks:", len(chunks))
    for chunk in chunks[:3]:
        print({**chunk, "text": chunk["text"][:60]})

    unique_ids = {chunk["id"] for chunk in chunks}
    print("All ids unique?", len(unique_ids) == len(chunks))