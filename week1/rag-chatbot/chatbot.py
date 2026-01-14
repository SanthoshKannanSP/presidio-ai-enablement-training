from utils.chatbot_utils import conversational_rag_query, create_session
from utils.vector_db import create_or_get_collection

collection = create_or_get_collection("suna-pana-consultancy")
session_id = create_session()

print("RAG Chatbot:")
query = input(">>>")
while query and query.strip()!="exit":
    response, sources = conversational_rag_query(collection, query,session_id)

    print()
    print("\nAnswer:", response)
    print("\nSources used:")
    for source in sources:
        print(f"- {source}")

    print()
    query = input(">>>")