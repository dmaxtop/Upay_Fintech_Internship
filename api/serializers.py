# serializers.py
from rest_framework import serializers
from api.models import Transaction
from api.models import Account

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'



class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'account_type', 'is_frozen']

class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'account_type', 'balance', 'is_frozen', 'user']
        read_only_fields = ['user', 'balance']