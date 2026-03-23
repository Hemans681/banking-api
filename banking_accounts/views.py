# from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from decimal import Decimal

from banking_accounts.models import Account
from .services import perform_transaction


class TransactionView(APIView):
    def post(self, request):
        try:
            operation = request.data.get("operation")
            account_id = request.data.get("account_id")
            amount = Decimal(request.data.get("amount"))

            account = perform_transaction(operation, account_id, amount)
            return Response({"balance": account.balance}, status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)


# Create your views here.
