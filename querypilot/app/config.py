from pathlib import Path

# Folder that contains everything: querypilot/
BASE_DIR = Path(__file__).resolve().parent.parent

# Data locations
DB_PATH = BASE_DIR / "data" / "querypilot.db"
DOCUMENTS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Local LLM
LLM_MODEL = "qwen2.5:3b"

# Chunking settings (we'll tune these in Phase 1)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

EMBED_MODEL = "nomic-embed-text"

COLLECTION_NAME = "policies"