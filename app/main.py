# app/main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# --- 1. DOWNLOADING AND SETUP ---
load_dotenv()

CHROMA_PATH = "chroma"

embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings_model)

retriever = db.as_retriever(search_kwargs={"k": 2}) # looking for the 2 most relevant documents.

# --- 2. ASSEMBLY OF THE RAG-CHAIN ​​---
template = """You are Baseline AIgent, an expert AI assistant for web developers.
Your goal is to provide accurate, reliable, and modern code solutions.
Answer the user's question based ONLY on the following context.
If the context doesn't contain the answer, say that you don't have enough information.
Explain your reasoning based on the feature's Baseline Status.

Context:
{context}

Question:
{question}
"""
prompt = ChatPromptTemplate.from_template(template)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()} # Step 1: Get the question and find relevant documents
    | prompt                                                  # Step 2: Paste the results into the prompt
    | llm                                                     # Step 3: Send the prompt to the AI ​​model
    | StrOutputParser()                                       # Step 4: Get the response in plain text
)

# --- 3. CHAIN ​​TESTING ---
if __name__ == "__main__":
    print("--- Testing RAG Chain ---")
    
    question = "Is CSS Nesting safe to use in production?"
    
    print(f"Question: {question}")
    
    # Let's start chain with a question
    response = rag_chain.invoke(question)
    
    print("Response:")
    print(response)

app = FastAPI()

@app.get("/")
def read_root():
    """This endpoint returns a welcome message."""
    return {"message": "Baseline AIgent server is running! 🚀"}