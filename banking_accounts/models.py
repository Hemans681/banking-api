from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.name}-{self.balance}"


class Transaction(models.Model):
    TRANSACTION_TYPE=(
        ('credit', 'Credit'),
        ('debit','Debit'),
        ('transfer', 'Transfer'),
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    type=models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.account.id}-{self.type}-{self.amount}"
