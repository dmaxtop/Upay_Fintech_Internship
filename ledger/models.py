from django.db import models    
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, realted_name= 'account')
    account_number = models.CharField(max_length=32, unique=True)
    balance_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Account"

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    card_number = models.CharField(max_length=16)
    description = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction of ${self.amount_usd} for {self.account.user.username} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    