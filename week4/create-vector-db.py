from utils.vector_db import process_and_add_documents, create_or_get_collection
from pathlib import Path

collection = create_or_get_collection("presidio-research")

folder_path = str(Path(__file__).parent / "docs")
process_and_add_documents(collection,folder_path)