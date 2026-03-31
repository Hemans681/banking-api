# from django.test import TestCase

# Create your tests here.
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from banking_accounts.models import Account, Transaction
from banking_accounts.services import perform_transaction, transfer_funds


@pytest.mark.django_db
def test_deposit(user):
    account = Account.objects.create(
        name="Test", balance=1000, user=user
    )  # pylint: disable=no-member
    perform_transaction("credit", account.id, 500, user=user)
    account.refresh_from_db()
    assert account.balance == 1500


@pytest.mark.django_db
def test_withdraw_success(user):
    account = Account.objects.create(name="test2", balance=1500, user=user)
    perform_transaction("debit", account.id, 1000, user=user)
    account.refresh_from_db()
    assert account.balance == 500


@pytest.mark.django_db
def test_withdraw_insufficient(user):
    account = Account.objects.create(
        name="Test", balance=100, user=user
    )  # pylint: disable=no-member

    with pytest.raises(ValueError):
        perform_transaction("debit", account.id, 200, user=user)


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="test123")


@pytest.mark.django_db
def test_transfer_success(user):
    from_account = Account.objects.create(name="test", balance=500, user=user)
    to_account = Account.objects.create(name="test", balance=0, user=user)
    transfer_funds(from_account.id, to_account.id, 200, user)
    from_account.refresh_from_db()
    to_account.refresh_from_db()
    assert from_account.balance == 300
    assert to_account.balance == 200


@pytest.mark.django_db
def test_transfer_fail(user):
    account = Account.objects.create(name="Test", balance=100, user=user)
    to_account = Account.objects.create(name="Test", balance=100, user=user)
    with pytest.raises(ValueError):
        transfer_funds(account.id, to_account.id, 200, user)


@pytest.mark.django_db
def test_transaction_history_success():
    # Arrange
    user = User.objects.create_user(username="testuser", password="test123")
    client = APIClient()
    client.force_authenticate(user=user)

    account = Account.objects.create(name="test", balance=1000, user=user)

    Transaction.objects.create(account=account, amount=100, type="credit")
    Transaction.objects.create(account=account, amount=50, type="debit")

    # Act
    response = client.get("/api/transaction/logs")

    # Assert
    assert response.status_code == 200
    assert response.data["message"] == "successful"
    assert len(response.data["data"]) == 2


@pytest.mark.django_db
def test_transaction_history_filter_by_account():
    user = User.objects.create_user(username="testuser", password="test123")
    client = APIClient()
    client.force_authenticate(user=user)

    acc1 = Account.objects.create(name="A", balance=1000, user=user)
    acc2 = Account.objects.create(name="B", balance=1000, user=user)

    Transaction.objects.create(account=acc1, amount=100, type="credit")
    Transaction.objects.create(account=acc2, amount=200, type="credit")

    response = client.get(f"/api/transaction/logs?account_id={acc1.id}")

    assert response.status_code == 200
    assert len(response.data["data"]) == 1
