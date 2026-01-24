from utils.rag.vector_db import create_or_get_collection
from utils.rag.search_utils import semantic_search

def read_file(query: str, collection_name: str):
    collection = create_or_get_collection(collection_name)
    
    return semantic_search(collection,query,10)