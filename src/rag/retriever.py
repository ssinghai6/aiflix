import chromadb
from typing import List, Tuple
from .data import SEED_KNOWLEDGE, KnowledgeItem
from ..config import Config
from ..utils import logger

class KnowledgeRetriever:
    """
    Retrieves knowledge chunks relevant to the query from ChromaDB.
    Falls back to seed data if DB is unavailable.
    """
    
    def __init__(self):
        self.db_path = Config.DATA_DIR / "chroma_db"
        self.collection = None
        
        try:
            if self.db_path.exists():
                client = chromadb.PersistentClient(path=str(self.db_path))
                # "aiflix_knowledge" must match the name in ingest_books.py
                self.collection = client.get_collection(name="aiflix_knowledge")
                logger.info(f"Connected to RAG database at {self.db_path}")
            else:
                logger.warning(f"RAG database not found at {self.db_path}. Using seed data.")
        except Exception as e:
            logger.warning(f"Failed to connect to ChromaDB: {e}. Using seed data.")

        # Fallback in-memory
        self.knowledge_base = SEED_KNOWLEDGE
        
    def retrieve(self, query: str, category: str = None, top_k: int = 3) -> List[KnowledgeItem]:
        """
        Retrieves top_k items matching the query.
        """
        # Try DB first
        if self.collection:
            try:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    where={"category": category} if category else None
                )
                
                items = []
                if results['documents']:
                    # Chroma returns list of lists (batch queries)
                    docs = results['documents'][0]
                    metas = results['metadatas'][0]
                    
                    for doc, meta in zip(docs, metas):
                        items.append(KnowledgeItem(
                            category=meta.get("category", "General"),
                            title=meta.get("source", "Book Excerpt"),  # Use filename as title
                            author="Inferred from source",
                            content=doc,
                            tags=[]
                        ))
                    return items
            except Exception as e:
                logger.error(f"ChromaDB query failed: {e}")
        
        # Fallback to simple keyword search
        logger.info("Falling back to in-memory keyword search.")
        results = []
        query_terms = set(query.lower().split())
        
        for item in self.knowledge_base:
            if category and item.category != category:
                continue
                
            score = 0
            content_lower = item.content.lower()
            title_lower = item.title.lower()
            
            for term in query_terms:
                if term in title_lower:
                    score += 3
                elif term in content_lower:
                    score += 1
                elif term in [t.lower() for t in item.tags]:
                    score += 2
            
            if score > 0:
                results.append((score, item))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in results[:top_k]]

    def format_context(self, items: List[KnowledgeItem]) -> str:
        """Formats retrieved items into a string for the context window."""
        if not items:
            return "No specific technical knowledge found."
            
        context_str = "### Relevant Technical Context:\n"
        for item in items:
            context_str += f"- **{item.title}** ({item.category}): {item.content[:500]}...\n" # Truncate long chunks
        return context_str
