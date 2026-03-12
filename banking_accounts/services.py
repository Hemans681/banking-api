from django.db import transaction

from banking_accounts.models import Account


@transaction.atomic
def perform_transaction(operation, account_id, amount):
    account = Account.objects.select_for_update().get(
        id=account_id
    )  # pylint:disable=no-member
    if operation == "deposit":
        account.balance += amount
    elif operation == "withdraw":
        if account.balance < amount:
            raise ValueError("Insufficient Funds")
        account.balance -= amount

    else:
        raise ValueError("Invalid operation")
    account.save()
    return account
