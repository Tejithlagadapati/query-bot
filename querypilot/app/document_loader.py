from pypdf import PdfReader

from app.config import DOCUMENTS_DIR


def load_document(file_path):
    """Read a .txt file and return its text, or None if it doesn't exist."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Document not found: {file_path}")
        return None


def load_pdf(file_path):
    """Read a PDF and return a list of {"page": number, "text": text}, one per page."""
    try:
        reader = PdfReader(file_path)
    except FileNotFoundError:
        print(f"Document not found: {file_path}")
        return []

    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text:
            continue  # empty page, or a scanned image with no text layer
        pages.append({"page": number, "text": text})
    return pages


def load_all_documents():
    """Load every .txt and .pdf in the documents folder.

    Returns a list of {"source": filename, "page": page number or None, "text": text}.
    """
    documents = []
    for path in sorted(DOCUMENTS_DIR.iterdir()):
        suffix = path.suffix.lower()

        if suffix == ".txt":
            text = load_document(path)
            if text:
                documents.append({"source": path.name, "page": None, "text": text})

        elif suffix == ".pdf":
            for page in load_pdf(path):
                documents.append({
                    "source": path.name,
                    "page": page["page"],
                    "text": page["text"],
                })
    return documents


if __name__ == "__main__":
    for doc in load_all_documents():
        print(doc["source"], doc["page"], len(doc["text"]))
        if doc["source"].endswith(".pdf"):
            print(doc["text"][:200])