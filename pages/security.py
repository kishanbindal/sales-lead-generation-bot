import streamlit as st

st.set_page_config(page_title="/security", page_icon=":shield:", layout="wide")
st.session_state["route"] = "/security"
st.title("Security Page")
st.caption("Bare-minimum security page. We'll add signals, nudges, and bot next")