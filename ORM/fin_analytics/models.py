from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator
from decimal import Decimal
from fin_analytics.managers import ActiveAccountManager, SuccessfulTransactionManager

class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fin_user_profile'
        indexes = [models.Index(fields=['email'])]

    def __str__(self):
        return self.username


class Account(models.Model):
    ACCOUNT_TYPES = [('SAVINGS', 'Savings'), ('CHECKING', 'Checking')]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)
    
    objects = models.Manager()  
    active_objects = ActiveAccountManager()  

    class Meta:
        db_table = 'fin_account'
        constraints = [
            models.CheckConstraint(
                condition=Q(balance__gte=0),
                name='balance_cannot_be_negative'
            )
        ]

    def __str__(self):
        return f"{self.account_number} ({self.account_type})"


class Merchant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'fin_merchant'

    def __str__(self):
        return self.name


class Transaction(models.Model):
    STATUS_CHOICES = [('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')]
    
    sender_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='sent_transactions')
    receiver_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='received_transactions', null=True, blank=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    success_objects = SuccessfulTransactionManager()

    class Meta:
        db_table = 'fin_transaction'
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"TX {self.id}: {self.amount} ({self.status})"


class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16, unique=True)
    expiry_date = models.DateField()
    is_blocked = models.BooleanField(default=False)

    class Meta:
        db_table = 'fin_card'

    def __str__(self):
        return f"Card Ending {self.card_number[-4:]}"