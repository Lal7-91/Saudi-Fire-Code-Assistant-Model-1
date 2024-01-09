import os
import openai
import streamlit as st

from PyPDF2 import PdfReader
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.vectorstores import faiss
FAISS = faiss.FAISS

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
#os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']



def load_and_extract_one_pdf(pdf_file_name):
    

    pdf_file_obj = open(os.path.join(os.getcwd(), "data", pdf_file_name), "rb")
    pdf_reader = PdfReader(pdf_file_obj)

    extracted_text = ""
    for page in pdf_reader.pages:
        extracted_text += page.extract_text()

    pdf_file_obj.close()
    return extracted_text

def creat_docs(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size= 2000, chunk_overlap= 200)
    docs = text_splitter.split_text(text)

    print(f"number of docs --> {len(docs)}")
    return docs


def creat_embedding(docs):
    embedding = OpenAIEmbeddings()
    doc_search = FAISS.from_texts(docs, embedding)
    return doc_search

def responce_chain(doc_search, prompt, LLM):
    from langchain.chains.question_answering import load_qa_chain

    chain = load_qa_chain(llm=LLM, chain_type="stuff")

    docs = FAISS.similarity_search(doc_search, prompt)

    response = chain.run(question=prompt, input_documents=docs)

    return response


conversation_history = []

def ask(file_name, question):

    global conversation_history

    LLM = ChatOpenAI(
        temperature= 1.0,
        model = "gpt-3.5-turbo",
        openai_api_key = openai.api_key
    )

    
    prompt = "\n".join(conversation_history) + "\n" + question

    response = responce_chain(
        creat_embedding(creat_docs(load_and_extract_one_pdf(file_name))), prompt=prompt, LLM = LLM)

    
    #conversation_history.append(response)

    return response

