import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema.output_parser import StrOutputParser
import os

st.title("🦜🔗 CV-as-a-bot")


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


def generate_response(input_text):
    # API Key expected to be loaded via an environment variable
    model = ChatOpenAI(
        model = "gpt-3.5-turbo",
        temperature = 0.7,
        n = 1,
        openai_api_key=openai_api_key
    )

    template = (
        "You are a helpful assistant that knows the curriculum vitae (CV) of Alexis Karadimos and answer to questions related to his skills & experience."
    )
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{query}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    # try:
    response = chain.invoke({"query": input_text})
    # except Exception as e:
    #     response = "There was a problem with the chatbot or Alexis has no skills. Please try again later or wait for him to learn something new."

    st.info(response)


with st.form("my_form"):
    text = st.text_area("Enter text:", "Which programming languages does @karadalex know?")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)