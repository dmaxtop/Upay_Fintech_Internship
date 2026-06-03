from django.db import models
from django.db.models import Q, F
from django.core.validators import MinValueValidator
from decimal import Decimal

# ─── CUSTOM MANAGERS ───
class ActiveAccountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class SuccessfulTransactionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='SUCCESS')

# ─── MODELS ───
class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fin_user_profile'
        indexes = [models.Index(fields=['email'])]


class Account(models.Model):
    ACCOUNT_TYPES = [('SAVINGS', 'Savings'), ('CHECKING', 'Checking')]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)
    
    objects = models.Manager()  # Default manager
    active_objects = ActiveAccountManager()  # Custom manager

    class Meta:
        db_table = 'fin_account'
        constraints = [
            models.CheckConstraint(
                check=Q(balance__gte=0), 
                name='balance_cannot_be_negative'
            )
        ]


class Merchant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'fin_merchant'


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


class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16, unique=True)
    expiry_date = models.DateField()
    is_blocked = models.BooleanField(default=False)

    class Meta:
        db_table = 'fin_card'