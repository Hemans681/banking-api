# from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from banking_accounts.models import Account
from banking_accounts.serializers import TransactionSerializer, TransferSerializer

from .services import perform_transaction, transfer_funds


class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = TransactionSerializer(data=request.data)
            if not serializer.is_valid():
                Response(
                    {"message": "unsuccessful", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = serializer.validated_data
            account = perform_transaction(
                data["operation"], data["account_id"], data["amount"], request.user
            )
            return Response(
                {"message": "successful", "balance": account.balance},
                status.HTTP_200_OK,
            )
        except Account.DoesNotExist:
            return Response(
                {"message": "unsuccessful", "error": "Account not found"},
                status.HTTP_404_NOT_FOUND,
            )
        except ValueError as e:
            return Response(
                {"message": "unsuccessful", "error": str(e)},
                status.HTTP_400_BAD_REQUEST,
            )


# Create your views here.
class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = TransferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "unsuccessful", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = serializer.validated_data
        try:

            from_account, to_account = transfer_funds(
                data["from_account"], data["to_account"], data["amount"], request.user
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
