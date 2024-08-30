import argparse
import os
from glob import glob
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from getembedding import get_embedding_function
from testRag import test_question
from interface import CHROMA_PATH
from PyPDF2 import PdfReader
from io import BytesIO
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
import streamlit as st
from pathlib import Path
from requests import post
from os.path import join, isfile

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_community.vectorstores.chroma import Chroma

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



    if (documents is not None):
        st.write("Successfully uploaded a PDF file.")
        save_folder = './pdfs'
        
        if not os.path.exists(save_folder):
          os.mkdir(save_folder)
          print("Folder %s created!" % save_folder)
        else:
          print("Folder %s already exists" % save_folder)
        
        save_path = Path(save_folder, documents.name)
        
        with open(save_path, mode='wb') as w:
            w.write(documents.getvalue())

        if save_path.exists():
            st.success(f'File {documents.name} is successfully saved in {save_folder}')
        else:
            st.error(f'Error saving file {documents.name}.')
            

        documents = load_documents(save_folder)
        st.write("1")
        if (documents):
            chunks = split_documents(documents)
            st.write("2")
            add_to_chroma(chunks) 
            st.write("3")
            st.write("Question about to be asked")
            question = st.text_input("Ask a question")
            st.write("Question has been asked")
            if st.button("Generate Answer"):
                if question:
                    response = test_question(question)
                    st.write(response) 
    else:
        st.write("Please upload a PDF file to proceed.")
            
        
   ##    documents = load_documents()

def load_documents(save_folder):
    if not os.path.exists(save_folder):
        st.write("Path doesn't exist")
        return None
    document_loader = PyPDFDirectoryLoader(save_folder)
    return document_loader.load()

#Commented out in this manner cause of streamlit

'''def load_pdf(uploaded_file):
    # Convert the uploaded file to a BytesIO object
    st.write("One")
    file_stream = BytesIO(uploaded_file.getvalue())
    st.write("Two")
    pdf_reader = PdfReader(file_stream)
    st.write("Three")
    pages = [pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages))]
    st.write("Four")
    documents = [Document(page_content=page_text) for page_text in pages]

    return documents'''

   
def add_to_chroma(chunks: list[Document]):
  # Load the existing database.
    st.write("a")
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )
    st.write("b")
    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)
    st.write('c')
    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    st.write(os.getenv("OPENAI_API_KEY"))
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
        CHUNK = 10
        API_ENDPOINT = '...'
        filelist = [filename for filename in glob(join(CHROMA_PATH, '*')) if isfile(filename)]
        for idx in range(0, len(filelist), CHUNK):
            files = [('file', open(fn, 'rb')) for fn in filelist[idx:idx+CHUNK]]
            post(API_ENDPOINT, files=files).raise_for_status()
            for _, fd in files:
                fd.close()
    else:
        st.write("Error: Database not found")

if __name__ == "__main__":
    main()



