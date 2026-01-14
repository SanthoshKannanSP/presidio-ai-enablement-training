from utils.vector_db import process_and_add_documents, create_or_get_collection

collection = create_or_get_collection("suna-pana-consultancy")

folder_path = "docs"
process_and_add_documents(collection,folder_path)