from django.urls import path

from .views import TransactionView, TransferView

urlpatterns = [
    path("transaction", TransactionView.as_view()),
    path("transfer/", TransferView.as_view()),
]
