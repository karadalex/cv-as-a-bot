import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema.output_parser import StrOutputParser
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader



st.title("🦜🔗 CV-as-a-bot")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


def generate_response(input_text):
    model = ChatOpenAI(
        model = "gpt-3.5-turbo",
        temperature = 0.7,
        n = 1,
        openai_api_key=openai_api_key
    )

    # RAG - Retrieval chain
    loader = WebBaseLoader("https://github.com/karadalex")
    docs = loader.load()
    # Debug documents
    # st.info(docs[0])
    # Create embeddings and store them as vectors
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)

    # Load PDF (e.g. CV as a pdf)
    loader = PyPDFLoader("data/cv.pdf")
    pages = loader.load_and_split()
    documents += pages
    # st.info(pages[0])

    st.info("Total documents: "+str(len(documents)))
    vector = DocArrayInMemorySearch.from_documents(documents, embeddings)

    # Similarity search for debugging
    docs = vector.similarity_search(input_text)
    # st.info(docs[0])

    # Prompt building
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant that knows the curriculum vitae (CV) of Alexis Karadimos and answer to questions related to his skills & experience.
    Ignore all Personally Identifiable Information that may appear in the context and do not show these or any other private data in your response.
    Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")
    document_chain = create_stuff_documents_chain(model, prompt)

    # Retriever
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # try:
    response = retrieval_chain.invoke({"input": input_text})
    # except Exception as e:
    #     response = "There was a problem with the chatbot or Alexis has no skills. Please try again later or wait for him to learn something new."

    st.info(response["answer"])


with st.form("my_form"):
    text = st.text_area("Enter text:", "Which programming languages has @karadalex used in his Github repositories?")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)