import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/transactions/"

st.set_page_config(page_title="Banking App", layout="centred")

st.title("🏦 Banking UI")

account_id = st.number_input("Account ID", min_value=1, step=1)
