import requests

BASE_URL = "http://127.0.0.1:8000/api"


def login_user(username, password):
    r = requests.post(
        f"{BASE_URL}/token/", json={"username": username, "password": password}
    )
    return r


def get_transactions(token):
    h = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE_URL}/transaction/logs", headers=h)


def get_accounts(token):
    h = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE_URL}/accounts/", headers=h)


def create_account(token, name, account_type):
    h = {"Authorization": f"Bearer {token}"}
    return requests.post(
        f"{BASE_URL}/accounts/",
        headers=h,
        json={"name": name, "account_type": account_type},
    )
