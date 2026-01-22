import os
import chromadb
from chromadb.utils import embedding_functions
from utils.document_utils import read_document
from pathlib import Path

chromd_db_path = str(Path(__file__).parent.parent / "chroma_db")

# Initialize ChromaDB client with persistence
client = chromadb.PersistentClient(path=chromd_db_path)

# Configure sentence transformer embeddings
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-mpnet-base-v2"
)

def create_or_get_collection(collection_name):
    # Create or get existing collection
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=sentence_transformer_ef,
        metadata={"hnsw:space": "cosine"}
    )

def process_document(file_path: str):
    """Process a single document and prepare it for ChromaDB"""
    try:
        # Read the document
        content = read_document(file_path)

        # Split into chunks
        chunks = split_text(content)

        # Prepare metadata
        file_name = os.path.basename(file_path)
        metadatas = [{"source": file_name, "chunk": i} for i in range(len(chunks))]
        ids = [f"{file_name}_chunk_{i}" for i in range(len(chunks))]

        return ids, chunks, metadatas
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return [], [], []

def split_text(text: str, chunk_size: int = 500):
    """Split text into chunks while preserving sentence boundaries"""
    sentences = text.replace('\n', ' ').split('. ')
    chunks = []
    current_chunk = []
    current_size = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # Ensure proper sentence ending
        if not sentence.endswith('.'):
            sentence += '.'

        sentence_size = len(sentence)

        # Check if adding this sentence would exceed chunk size
        if current_size + sentence_size > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_size = sentence_size
        else:
            current_chunk.append(sentence)
            current_size += sentence_size

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def add_to_collection(collection, ids, texts, metadatas):
    """Add documents to collection in batches"""
    if not texts:
        return

    batch_size = 100
    for i in range(0, len(texts), batch_size):
        end_idx = min(i + batch_size, len(texts))
        collection.add(
            documents=texts[i:end_idx],
            metadatas=metadatas[i:end_idx],
            ids=ids[i:end_idx]
        )

def process_and_add_documents(collection, folder_path: str):
    """Process all documents in a folder and add to collection"""
    files = [os.path.join(folder_path, file) 
             for file in os.listdir(folder_path) 
             if os.path.isfile(os.path.join(folder_path, file))]

    for file_path in files:
        print(f"Processing {os.path.basename(file_path)}...")
        ids, texts, metadatas = process_document(file_path)
        add_to_collection(collection, ids, texts, metadatas)
        print(f"Added {len(texts)} chunks to collection")

