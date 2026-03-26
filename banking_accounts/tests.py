# from django.test import TestCase

# Create your tests here.
import pytest
from django.contrib.auth.models import User

from banking_accounts.models import Account
from banking_accounts.services import perform_transaction


@pytest.mark.django_db
def test_deposit(user):
    account = Account.objects.create(
        name="Test", balance=1000, user=user
    )  # pylint: disable=no-member
    perform_transaction("credit", account.id, 500, user=user)
    account.refresh_from_db()
    assert account.balance == 1500


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
