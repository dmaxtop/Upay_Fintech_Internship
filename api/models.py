# api/models.py
from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    ACCOUNT_TYPES = [('checking', 'Checking'), ('savings', 'Savings')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=30, choices=ACCOUNT_TYPES, default='checking')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_frozen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account_number} ({self.user.username})"

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_reversed = models.BooleanField(default=False)

    def __str__(self):
        return f"Tx {self.id}: {self.amount} -> {self.account.account_number}"