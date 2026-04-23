from django.urls import path

from .views import (
    AccountListView,
    TransactionHistoryView,
    TransactionView,
    TransferView,
)

urlpatterns = [
    path("transaction", TransactionView.as_view()),
    path("transfer/", TransferView.as_view()),
    path("transaction/logs", TransactionHistoryView.as_view()),
    path("accounts/", AccountListView.as_view()),
    path,
]
