import argparse
import os
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from getembedding import get_embedding_function
from langchain_community.vectorstores.chroma import Chroma
from testRag import test_question
from interface import CHROMA_PATH
from PyPDF2 import PdfReader
from io import BytesIO
import streamlit as st


def main():
    st.title("TextbookAI")
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()

    button = st.button("Clear database")
    if button:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    
    
    documents = st.file_uploader(label="Choose a PDF file", type="pdf")

    if documents is not None:
        documents = load_pdf(documents)
        chunks = split_documents(documents)
        add_to_chroma(chunks) #Issue here
        question = st.text_input("Ask a question")
        if st.button("Generate Answer"):
            if question != None:
                response = test_question(question)
                st.write(response)
            
        
   ##    documents = load_documents()
    
    
    
    
    
    

    


#def load_documents():
  #document_loader = PyPDFDirectoryLoader('data')
  #return document_loader.load()

#Commented out in this manner cause of streamlit

def load_pdf(uploaded_file):
    # Convert the uploaded file to a BytesIO object
    file_stream = BytesIO(uploaded_file.getvalue())
    pdf_reader = PdfReader(file_stream)
    pages = [pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages))]
    documents = [Document(page_content=page_text) for page_text in pages]

    return documents

   


def add_to_chroma(chunks: list[Document]):
  # Load the existing database.
  db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

  # Calculate Page IDs.
  chunks_with_ids = calculate_chunk_ids(chunks)

  # Add or Update the documents.
  existing_items = db.get(include=[])  # IDs are always included by default
  existing_ids = set(existing_items["ids"])
  print(f"Number of existing documents in DB: {len(existing_ids)}")

  # Only add documents that don't exist in the DB.
  new_chunks = []
  for chunk in chunks_with_ids:
      if chunk.metadata["id"] not in existing_ids:
          new_chunks.append(chunk)

  if len(new_chunks):
      print(f"Adding new documents: {len(new_chunks)}")
      new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
      db.add_documents(new_chunks, ids=new_chunk_ids) #error
      db.persist()
  else:
      print("No new documents to add")


def calculate_chunk_ids(chunks):

# Page Source : Page Number : Chunk Index
    
    last_page_id = None
    current_chunk_index = 0
    
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"
    
        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
    
        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
    
        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id
    
    return chunks


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=128,
        chunk_overlap=64,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()



