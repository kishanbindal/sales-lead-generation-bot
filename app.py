import streamlit as st

def chatbot_state():
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("generated_lead", False)
    st.session_state.setdefault("kb_ready", False)
    st.session_state.setdefault("faq_path", None)
    st.session_state.setdefault("nudge_path", None)

chatbot_state()

st.title("Lead Generation Bot")
st.write("Use the sidebar to navigate between pages")

if st.session_state.kb_ready and st.session_state.faq_path and st.session_state.nudge_path:
    st.toast("Bot is ready to chat")
    st.switch_page("pages/chat_page.py")
else:
    st.switch_page("pages/config_loader.py")