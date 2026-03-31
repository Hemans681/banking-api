from django.db import transaction

from banking_accounts.models import Account, Transaction


@transaction.atomic
def perform_transaction(operation, account_id, amount, user):
    account = Account.objects.select_for_update().get(
        id=account_id, user=user
    )  # pylint:disable=no-member
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


@transaction.atomic
def transfer_funds(from_account_id, to_account_id, amount, user):

    from_account = Account.objects.select_for_update().get(
        id=from_account_id, user=user
    )
    to_account = Account.objects.select_for_update().get(id=to_account_id, user=user)

    if from_account.balance < amount:
        raise ValueError("Not enough balance to perform transaction")

    # debit
    from_account.balance -= amount
    from_account.save()
    # credit
    to_account.balance += amount
    to_account.save()

    # transaction_logs
    Transaction.objects.create(account=from_account, amount=amount, type="debit")
    Transaction.objects.create(account=to_account, amount=amount, type="credit")
    return from_account, to_account
