import pandas as pd
import streamlit as st

from clients.api import get_accounts, get_transactions


def show_dashboard():
    st.title("🏦 Dashboard")

    col1, col2 = st.columns([6, 1])

    with col2:
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.refresh = None
            st.rerun()

    st.divider()
    acc = get_accounts(st.session_state.token)
    st.write(acc)
    if acc.ok:
        accounts = acc.json()
        if accounts:
            st.dataframe(pd.DataFrame(accounts), use_container_width=True)
        else:
            st.info("No Accounts Found")
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
