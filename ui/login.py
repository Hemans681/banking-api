import streamlit as st

from clients.api import login_user


def show_login():
    st.title("Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        r = login_user(u, p)
        if r.ok:
            data = r.json()
            st.session_state.token = data["access"]
            st.session_state.refresh = data["refresh"]
            st.rerun()
        else:
            st.error(r.text)
