import streamlit as st
import json
from utils.vector_store import VectorStore
import os

st.title("Lead Bot Config Loader")

if st.session_state.kb_ready and st.session_state.faq_path and st.session_state.nudge_path:
    st.toast("Bot is ready to chat")
else:
    st.toast("Bot is not ready to chat, please Configure the bot with the required files to continue")

faq_file = st.file_uploader("Upload FAQ JSON", type="json")
kb_file = st.file_uploader("Upload Knowledge Base TXT", type="txt")
nudge_file = st.file_uploader("Upload Nudges JSON", type="json")

if faq_file:
    """
    Store the FAQ into a JSON File
    Set the state of FAQ configuration so that the chatbot can use it in the future.
    """
    faq_data = json.load(faq_file)
    st.write("FAQ Data:", faq_data)
    save_dir = "config"
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, "faq_data.json")
    with open(path, "w") as f:
        json.dump(faq_data, f)
    st.session_state.faq_path = path

if kb_file:
    """
    Create a FAISS Vector Store from the Knowledge Base txt document
    This would enable the chatbot to use the Knowledge Base for retrieval.
    """
    try:
        print("Processing Knowledge Base", kb_file)
        save_dir = "config"
        save_path = os.path.join(save_dir, "kb_data.txt")
        with open(save_path, "w") as f:
            f.write(kb_file.read().decode("utf-8"))
        vs = VectorStore("faiss_store_2")
        ingestion_status= vs.ingest_data(save_path)
        if ingestion_status:
            st.session_state.kb_ready = True
            st.toast("Knowledge Base ingested successfully")
        else:
            st.session_state.kb_ready = False
            st.toast("Knowledge Base ingestion failed")
    except Exception as e:
        st.session_state.kb_ready = False
        st.toast("Knowledge Base ingestion failed")
        print(e)

if nudge_file:
    """
    Store the Nudges into a JSON File
    Set the state of Nudge configuration so that the chatbot can use it in the future.
    """
    nudges = json.load(nudge_file)
    st.write("Nudges Config:", nudges)
    save_dir = "config"
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, "nudge_data.json")
    with open(path, "w") as f:
        json.dump(nudges, f)
    st.session_state.nudge_path = path
