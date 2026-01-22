from chromadb.api.models.Collection import Collection


def semantic_search(collection: Collection, query: str, n_results: int = 2):
    """Perform semantic search on the collection"""
    results = collection.query(query_texts=[query], n_results=n_results)
    return "\n\n".join(results["documents"][0])