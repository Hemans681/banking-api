import streamlit as st

from ui.dashboard import show_dashboard
from ui.login import show_login

st.set_page_config(page_title="Banking App", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None

token = st.session_state.get("token")
if st.session_state.token:
    show_dashboard()
else:
    show_login()
