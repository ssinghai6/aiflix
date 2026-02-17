from src.rag.retriever import KnowledgeRetriever

def main():
    retriever = KnowledgeRetriever()
    
    print("\n=== DEMO: Screenplay Agent Context ===")
    # Simulate what the Screenplay Agent does
    query = "hero structure"
    print(f"Agent is thinking about: '{query}'")
    
    # It searches the 'Screenwriting' category in src/rag/data.py
    items = retriever.retrieve(query, category="Screenwriting")
    
    print(f"Found {len(items)} reference(s) to inject into prompt:")
    for item in items:
        print(f"\n[SOURCE: {item.title} by {item.author}]")
        print(f"CONTENT: {item.content}")
        print("-" * 40)

    print("\n=== DEMO: DOP Agent Context ===")
    # Simulate DOP Agent
    query = "lighting camera"
    print(f"Agent is thinking about: '{query}'")
    
    items = retriever.retrieve(query, category="Cinematography")
    
    for item in items:
        print(f"\n[SOURCE: {item.title}]")
        print(f"CONTENT: {item.content}")

if __name__ == "__main__":
    main()
