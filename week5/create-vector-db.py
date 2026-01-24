from utils.constants import FINANCE_DOCS_COLLECTIION, IT_DOCS_COLLECTION, PROJECT_ROOT
from utils.rag.vector_db import create_or_get_collection, process_and_add_documents

it_docs_collection = create_or_get_collection(IT_DOCS_COLLECTION)
folder_path = str(PROJECT_ROOT / "it_docs")
process_and_add_documents(it_docs_collection, folder_path)

finance_docs_collection = create_or_get_collection(FINANCE_DOCS_COLLECTIION)
folder_path = str(PROJECT_ROOT / "finance_docs")
process_and_add_documents(finance_docs_collection, folder_path)
