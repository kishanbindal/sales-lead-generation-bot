import streamlit as st

# 1) Drop this CSS once on the page
st.markdown("""
<style>
  /* position only the button that comes right after the anchor */
  #fab-anchor + div.stButton {
    position: fixed;
    right: 16px;
    bottom: 16px;
    z-index: 10000;
  }
  #fab-anchor + div.stButton > button {
    width: 56px; height: 56px; border-radius: 50%;
    border: 0; font-size: 22px;
  }
</style>
""", unsafe_allow_html=True)

# 2) Put the anchor BEFORE the button (no containers/columns around them)
st.markdown('<div id="fab-anchor"></div>', unsafe_allow_html=True)
if st.button("💬", key="fab_toggle"):
    st.write("clicked")