# from django.test import TestCase

# Create your tests here.
import pytest

from banking_accounts.models import Account
from banking_accounts.services import perform_transaction


@pytest.mark.django_db
def test_deposit():
    account = Account.objects.create(
        name="Test", balance=1000
    )  # pylint: disable=no-member
    perform_transaction("deposit", account.id, 500)
    account.refresh_from_db()
    assert account.balance == 1500


@pytest.mark.django_db
def test_withdraw_insufficient():
    account = Account.objects.create(
        name="Test", balance=100
    )  # pylint: disable=no-member

    with pytest.raises(ValueError):
        perform_transaction("withdraw", account.id, 200)
