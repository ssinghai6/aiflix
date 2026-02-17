import os
import chromadb
from chromadb.config import Settings
from pypdf import PdfReader
from pathlib import Path
from tqdm import tqdm
from src.config import Config, logger

def ingest_books():
    """
    Reads PDFs from Books/ directory, chunks them, and stores embeddings in ChromaDB.
    """
    books_dir = Config.PROJECT_ROOT / "Books"
    db_path = Config.DATA_DIR / "chroma_db"
    
    if not books_dir.exists():
        logger.error(f"Books directory not found at {books_dir}")
        return

    logger.info(f"Initializing ChromaDB at {db_path}...")
    client = chromadb.PersistentClient(path=str(db_path))
    
    # Create or get collection
    # We use the default embedding function (all-MiniLM-L6-v2) which runs locally
    collection = client.get_or_create_collection(name="aiflix_knowledge")
    
    files = list(books_dir.glob("*.pdf"))
    logger.info(f"Found {len(files)} PDF books to ingest.")
    
    for file_path in files:
        logger.info(f"Processing: {file_path.name}")
        try:
            reader = PdfReader(file_path)
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
            
            # Simple chunking strategy (e.g., 1000 characters with overlap)
            chunk_size = 1000
            overlap = 200
            chunks = []
            metadatas = []
            ids = []
            
            for i in range(0, len(text_content), chunk_size - overlap):
                chunk = text_content[i:i + chunk_size]
                if len(chunk) < 50:  # Skip tiny chunks
                    continue
                
                # Determine category based on filename keywords (heuristic)
                category = "General"
                lower_name = file_path.name.lower()
                if "cinematography" in lower_name or "light" in lower_name or "camera" in lower_name:
                    category = "Cinematography"
                elif "screen" in lower_name or "story" in lower_name or "hero" in lower_name:
                    category = "Screenwriting"
                
                chunks.append(chunk)
                metadatas.append({
                    "source": file_path.name,
                    "category": category,
                    "chunk_id": i
                })
                ids.append(f"{file_path.name}_{i}")
            
            # Batch upsert to avoid memory issues
            batch_size = 100
            for j in tqdm(range(0, len(chunks), batch_size), desc=f"Embedding {file_path.name}"):
                collection.upsert(
                    documents=chunks[j:j+batch_size],
                    metadatas=metadatas[j:j+batch_size],
                    ids=ids[j:j+batch_size]
                )
                
        except Exception as e:
            logger.error(f"Failed to process {file_path.name}: {e}")

    logger.info(f"Ingestion complete. Collection now has {collection.count()} documents.")

if __name__ == "__main__":
    ingest_books()
