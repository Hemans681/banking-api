import streamlit as st
import pandas as pd
from clients.api import get_transactions

def show_dashboard():
    st.title("🏦 Dashboard")

    col1, col2 = st.columns([6, 1])

    with col2:
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.refresh = None
            st.rerun()

    st.divider()

    r = get_transactions(st.session_state.token)

    if r.ok:
        data = r.json().get("data", [])

        st.subheader("Transactions")

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No transactions yet.")
    else:
        st.error(r.text)