# from django.shortcuts import render
from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from banking_accounts.models import Account

from .services import perform_transaction, transfer_funds


class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            operation = request.data.get("operation")
            account_id = request.data.get("account_id")
            amount = Decimal(request.data.get("amount"))

            account = perform_transaction(operation, account_id, amount, request.user)
            return Response({"balance": account.balance}, status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)


# Create your views here.
class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from_account = request.data.get("from_account")
        to_account = request.data.get("to_account")
        amount = Decimal(str(request.data.get("amount")))

        try:
            from_account, to_account = transfer_funds(
                from_account, to_account, amount, request.user
            )
            return Response(
                {
                    "message": "successful",
                    "from_account_balance": from_account.balance,
                    "to_account_balance": to_account.balance,
                }
            )
        except ValueError as err:
            return Response(
                {"message": "unsuccessful", "error": str(err)},
                status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            return Response(
                {"message": "unsuccessful", "error": str(err)},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
