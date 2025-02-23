from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from global_vars import DATA_DIR, CHROMA_PATH
from dotenv import load_dotenv
import openai
import os
import shutil

# load api key as environment variable
load_dotenv()

openai.api_key = os.environ['API_KEY']

def generate_chroma_db(DATA_DIR, CHROMA_PATH):
    documents = load_documents(DATA_DIR)
    chunks = split_text(documents)
    save_to_chroma(chunks, CHROMA_PATH)

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    #print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    return chunks

def load_documents(DATA_DIR):
    loader = DirectoryLoader(DATA_DIR, glob="*.md")
    documents = loader.load()
    return documents

def save_to_chroma(chunks: list[Document], CHROMA_PATH):
    # clear database if other data is present
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(api_key=os.environ['API_KEY']), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}")

if __name__ == "__main__":
    generate_chroma_db(DATA_DIR, CHROMA_PATH)