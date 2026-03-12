# from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import perform_transaction


class TransactionView(APIView):
    def post(self, request):
        try:
            operation = request.data.get("operation")
            account_id = request.data.get("account_id")
            amount = float(request.data.get("amount"))

            account = perform_transaction(operation, account_id, amount)
            return Response({"balance": account.balance}, status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)


# Create your views here.
