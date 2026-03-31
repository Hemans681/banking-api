from django.urls import path

from .views import TransactionHistoryView, TransactionView, TransferView

urlpatterns = [
    path("transaction", TransactionView.as_view()),
    path("transfer/", TransferView.as_view()),
    path("transaction/logs", TransactionHistoryView.as_view()),
]
