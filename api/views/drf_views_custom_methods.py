from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.models import Account, Transaction
from api.serializers import (
    AccountListSerializer, 
    AccountDetailSerializer, 
    TransactionSerializer
)

class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    # Task 4: Filter by logged-in user
    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    # Task 4: Different serializers for list vs detail
    def get_serializer_class(self):
        if self.action == 'list':
            return AccountListSerializer
        return AccountDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Task 3: /accounts/{id}/freeze
    @action(detail=True, methods=['post'])
    def freeze(self, request, pk=None):
        account = self.get_object()
        account.is_frozen = not account.is_frozen
        account.save()
        state = "frozen" if account.is_frozen else "unfrozen"
        return Response({'status': f'Account {state}.'})

    # Task 3: /accounts/{id}/statement
    @action(detail=True, methods=['get'])
    def statement(self, request, pk=None):
        account = self.get_object()
        transactions = account.transactions.all().order_by('-timestamp')
        serializer = TransactionSerializer(transactions, many=True)
        return Response({
            'account_number': account.account_number,
            'balance': account.balance,
            'transactions': serializer.data
        })


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    # Task 4: Filter transactions by user's accounts
    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user)

    def create(self, request, *args, **kwargs):
        account = Account.objects.get(pk=request.data.get('account'))
        if account.is_frozen:
            return Response({'error': 'Account is frozen.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    # Task 3: /transactions/{id}/reverse
    @action(detail=True, methods=['post'])
    def reverse(self, request, pk=None):
        transaction = self.get_object()
        if transaction.is_reversed:
            return Response({'error': 'Already reversed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Reverse balance
        account = transaction.account
        account.balance -= transaction.amount
        account.save()

        transaction.is_reversed = True
        transaction.save()
        return Response({'status': 'Transaction reversed.'})