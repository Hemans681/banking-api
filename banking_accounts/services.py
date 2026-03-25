from decimal import Decimal

from django.db import transaction

from banking_accounts.models import Account, Transaction


@transaction.atomic
def perform_transaction(operation, account_id, amount, user):
    account = Account.objects.select_for_update().get(
        id=account_id, user=user
    )  # pylint:disable=no-member
    amount = Decimal(amount)
    if operation == "credit":
        account.balance += amount
    elif operation == "debit":
        if account.balance < amount:
            raise ValueError("Insufficient Funds")
        account.balance -= amount

    else:
        raise ValueError("Invalid operation")
    account.save()

    # Transaction Record
    Transaction.objects.create(
        account=account,
        amount=amount,
        type=operation,
    )
    return account
