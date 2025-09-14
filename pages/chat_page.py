import streamlit as st
from pydantic import BaseModel
from typing import Literal, Annotated
import json 
from utils.vector_store import VectorStore
from fuzzywuzzy import fuzz
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
st.set_page_config(page_title="Sales Bot Demo", page_icon=":robot:", layout="wide")
from langchain_core.tools import tool
from utils.chat import chat
from utils.tools import save_generated_lead



class Message(BaseModel):
    """
    pydantic model for message in the chat
    """
    role: Literal["user", "assistant"]
    content: Annotated[str, ""]


def answer_faq(question: str, faq_data_path: str, threshold: int = 80):
    """
    This function is used to answer the faq question from the faq data
    Function uses fuzzywuzzy to match the question with the faq data
    """
    with open(faq_data_path, "r") as f:
        faq_data=json.load(f)
    faq_data=faq_data["faqs"]
    for doc in faq_data:
        questions = [doc['q']] + doc['q_variants']
        score = max(fuzz.partial_ratio(question, q) for q in questions)
        if score >= threshold:
            return f"""
            Answer:     
            {doc['a_md']}

            Cited Sources:
            Title: {doc['source']['title']}\n
            Location: {doc['source']['loc']}\n
            URL: {doc['source']['url']}
            """
    return None

def submit_message(message:Message):
    """
    This function is used to submit the message to the chatbot
    If FAQ is answerable, it will answer the question from the faq data
    If FAQ is not answerable, it will use the vector store to answer the question

    A nudge is provided to the user after 2 responses from the chatbot (FAQ + Retrieval)
    """
    message_history = st.session_state.messages
    st.session_state.messages.append(message)
    if message.role == "user":
        with st.chat_message("user"):
            st.write(message.content)
        faq_answer = answer_faq(message.content, st.session_state.faq_path, 80)
        # faq_answer = answer_faq(message.content, "data/faq_data.json", 80)
        if faq_answer:
            st.session_state.messages.append(Message(role="assistant", content=faq_answer))
            with st.chat_message("assistant"):
                st.write(faq_answer)
        else:
            vs = VectorStore("faiss_store")
            output = vs.vector_search(message.content, 3)
            output = chat(message.content, output, [save_generated_lead], message_history)
            print(output.keys())
            st.session_state.messages.append(Message(role="assistant", content=output["output"]))
            with st.chat_message("assistant"):
                st.write(output["output"])
    message_history = st.session_state.messages
    if not st.session_state.generated_lead and len(message_history) >= 4:
        json_data = json.load(open(st.session_state.nudge_path))
        nudge_text = json_data["email_after_4"]["nudge_text"]
        st.toast(nudge_text)

def chatbot():
    """
    This function is used to render the chatbot UI
    """
    st.title("Chatbot")
    with st.container():
        for message in st.session_state.messages:
            with st.chat_message(message.role):
                st.write(message.content)
    user_input = st.chat_input("Enter your message")
    if user_input:
        submit_message(
            Message(role="user", content=user_input)
        )

# print(st.session_state)
# chatbot_state()
if st.session_state.kb_ready and st.session_state.faq_path and st.session_state.nudge_path:
    """
    Chatbot is ready ince all the required configuration files are uploaded.
    """
    chatbot()
else:
    st.error("Please upload the required files to continue")