# scripts/knowledge_base_builder.py
import json
import os
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# Path to the file with processed data
PROCESSED_DATA_FILE = "data/processed_features.json"
# Path where vector database will be stored
CHROMA_PATH = "chroma"

def main():
    """
    The main function for creating and saving a vector knowledge base.
    """
    # --- 1. Uploading processed documents ---
    print(f"Loading processed documents from {PROCESSED_DATA_FILE}...")
    try:
        with open(PROCESSED_DATA_FILE, 'r', encoding='utf-8') as f:
            documents_list = json.load(f)
    except FileNotFoundError:
        print(f"Error: Processed data file not found at {PROCESSED_DATA_FILE}")
        print("Please run 'scripts/data_processor.py' first.")
        return

    print(f"Loaded {len(documents_list)} documents.")

    # --- 2. Creating Embeddings and Saving to ChromaDB ---
    print("Creating embeddings and saving to ChromaDB. This may take a moment...")

    # Creating a model for Google embeddings
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Create a Chroma database from documents.
    db = Chroma.from_texts(
        documents_list, 
        embeddings_model, 
        persist_directory=CHROMA_PATH
    )
    
    print(f"Successfully created and saved database to {CHROMA_PATH}")

    # --- 3. Retriever testing ---
    print("\n--- Testing the retriever ---")
    query = "CSS Nesting"
    
    # Looking for documents that are most similar to request.
    # Get the 2 most relevant results.
    results = db.similarity_search(query, k=2)

    print(f"Query: '{query}'")
    print(f"Found {len(results)} relevant documents.")
    
    if results:
        print("--- Top Result ---")
        # results[0].page_content contains the text of the found document
        print(results[0].page_content)
        print("------------------")

if __name__ == "__main__":
    main()