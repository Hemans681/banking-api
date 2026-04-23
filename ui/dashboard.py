import pandas as pd
import streamlit as st

from clients.api import get_accounts, get_transactions


def show_dashboard():
    st.title("🏦 Banking Dashboard")

    col1, col2 = st.columns([6, 1])

    with col2:
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.refresh = None
            st.rerun()

    st.divider()
    # Accounts Section
    st.subheader("Your Accounts")

    acc = get_accounts(st.session_state.token)
    # st.write(acc.json)

    if acc.ok:
        accounts = acc.json()
        if accounts:
            st.dataframe(pd.DataFrame(accounts), use_container_width=True)
        else:
            st.info("No Accounts Found")
    else:
        st.error("Could not load accounts")

    st.divider()

    # Transaction Section

    txn = get_transactions(st.session_state.token)

    if txn.ok:
        data = txn.json().get("data", [])

        st.subheader("Recent Transactions")

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No transactions yet.")
    else:
        st.error(txn.text)
