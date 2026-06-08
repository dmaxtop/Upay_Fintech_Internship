# api/serializers.py
from rest_framework import serializers
from .models import Account, Transaction

class AccountListSerializer(serializers.ModelSerializer):
    """Task 4: Lightweight serialization context for lists (excludes balance info)"""
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'account_type', 'is_frozen']

class AccountDetailSerializer(serializers.ModelSerializer):
    """Task 4: Complete high-fidelity fields representation for details views"""
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'account_type', 'balance', 'is_frozen', 'user']
        read_only_fields = ['user', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'