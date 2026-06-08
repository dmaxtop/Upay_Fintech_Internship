import os
import django
from django.conf import settings
from django.core.management import call_command

# 1. Bootstrapping inline Django configuration with an in-memory SQLite DB
if not settings.configured:
    settings.configure(
        SECRET_KEY='production_testing_secret_key',
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'rest_framework',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
    )
    django.setup()

    # Create base authentication tables and application models
    call_command('migrate', verbosity=0, interactive=False)
    from django.db import connection
    with connection.schema_editor() as schema_editor:
        from models import Account, Transaction
        schema_editor.create_model(Account)
        schema_editor.create_model(Transaction)

# 2. Test Execution Engine Imports
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from models import Account, Transaction
from api_views import AccountViewSet, TransactionViewSet  # Adjust if saved elsewhere

def run_production_api_tests():
    factory = APIRequestFactory()
    
    print("Executing Production API Feature & Constraints Verification...")
    print("=" * 65)

    # Setup baseline mock users
    user_alpha = User.objects.create_user(username='user_alpha', password='testpassword123')
    user_beta = User.objects.create_user(username='user_beta', password='testpassword123')

    # Create an initial account owned by user_alpha directly through the ORM for testing
    account_alpha = Account.objects.create(
        user=user_alpha, 
        account_number="ACC-ALPHA-777", 
        account_type="checking", 
        balance=1000.00
    )

    # =========================================================================
    # Test 1: User Isolation & Queryset Overrides (Task 4)
    # =========================================================================
    print("\n▶ Testing Task 4: get_queryset User Isolation")
    view_list = AccountViewSet.as_view({'get': 'list'})
    
    # Requesting as User Alpha (Should see 1 account)
    req_alpha = factory.get('/api/accounts/')
    force_authenticate(req_alpha, user=user_alpha)
    res_alpha = view_list(req_alpha)
    
    # Requesting as User Beta (Should see 0 accounts)
    req_beta = factory.get('/api/accounts/')
    force_authenticate(req_beta, user=user_beta)
    res_beta = view_list(req_beta)
    
    print(f"   [User Alpha] Accounts visible: {len(res_alpha.data)}")
    print(f"   [User Beta]  Accounts visible: {len(res_beta.data)}")
    if len(res_alpha.data) == 1 and len(res_beta.data) == 0:
        print("   ✅ Pass: Users can only see their own accounts.")

    # =========================================================================
    # Test 2: Serializer Context Switching (Task 4)
    # =========================================================================
    print("\n▶ Testing Task 4: Contextual Serializer Class Switching")
    view_detail = AccountViewSet.as_view({'get': 'retrieve'})
    
    # Detail View Request
    req_detail = factory.get(f'/api/accounts/{account_alpha.pk}/')
    force_authenticate(req_detail, user=user_alpha)
    res_detail = view_detail(req_detail, pk=account_alpha.pk)
    
    print(f"   [List Action Fields]:   {list(res_alpha.data[0].keys())}")
    print(f"   [Detail Action Fields]: {list(res_detail.data.keys())}")
    if 'balance' in res_detail.data and 'balance' not in res_alpha.data[0]:
        print("   ✅ Pass: List uses AccountListSerializer (no balance), Detail uses AccountDetailSerializer.")

    # =========================================================================
    # Test 3: Custom Action - Account Freeze & Validation Guard (Task 3 & 4)
    # =========================================================================
    print("\n▶ Testing Task 3 & 4: Custom @action 'freeze' & Guard Verification")
    view_freeze = AccountViewSet.as_view({'post': 'freeze'})
    
    # Toggle Freeze to True
    req_freeze = factory.post(f'/api/accounts/{account_alpha.pk}/freeze/')
    force_authenticate(req_freeze, user=user_alpha)
    res_freeze = view_freeze(req_freeze, pk=account_alpha.pk)
    print(f"   [Freeze Trigger Response]: {res_freeze.data.get('status')}")

    # Verify transaction processing block on frozen status
    view_tx_create = TransactionViewSet.as_view({'post': 'create'})
    req_tx = factory.post('/api/transactions/', data={"account": account_alpha.pk, "amount": "150.00"}, format='json')
    force_authenticate(req_tx, user=user_alpha)
    res_tx = view_tx_create(req_tx)
    print(f"   [Tx Request on Frozen Account Status]: {res_tx.status_code}")
    if res_tx.status_code == 400:
        print("   ✅ Pass: Custom action successfully froze account and blocked transactions.")

    # Unfreeze account for remaining test blocks
    view_freeze(req_freeze, pk=account_alpha.pk)

    # =========================================================================
    # Test 4: Custom Action - Statement Endpoint (Task 3)
    # =========================================================================
    print("\n▶ Testing Task 3: Custom @action 'statement'")
    # Explicitly seed an approved transaction string
    tx_mock = Transaction.objects.create(account=account_alpha, amount=250.00)
    
    view_statement = AccountViewSet.as_view({'get': 'statement'})
    req_statement = factory.get(f'/api/accounts/{account_alpha.pk}/statement/')
    force_authenticate(req_statement, user=user_alpha)
    res_statement = view_statement(req_statement, pk=account_alpha.pk)
    
    print(f"   [Statement Payloads Returned Keys]: {list(res_statement.data.keys())}")
    print(f"   [Statement Transaction Entries Count]: {len(res_statement.data.get('transactions', []))}")
    if 'transactions' in res_statement.data and len(res_statement.data['transactions']) == 1:
        print("   ✅ Pass: Bank statement context successfully consolidated.")

    # =========================================================================
    # Test 5: Custom Action - Transaction Reversal (Task 3)
    # =========================================================================
    print("\n▶ Testing Task 3: Custom @action 'reverse'")
    view_reverse = TransactionViewSet.as_view({'post': 'reverse'})
    req_reverse = factory.post(f'/api/transactions/{tx_mock.pk}/reverse/')
    force_authenticate(req_reverse, user=user_alpha)
    res_reverse = view_reverse(req_reverse, pk=tx_mock.pk)
    
    account_alpha.refresh_from_db()
    tx_mock.refresh_from_db()
    
    print(f"   [Reversal Action Response]: {res_reverse.data.get('status')}")
    print(f"   [Post-Reversal Account Balance]: ${account_alpha.balance}")
    print(f"   [Transaction Is Reversed Flag]:  {tx_mock.is_reversed}")
    if tx_mock.is_reversed and account_alpha.balance == 750.00:
        print("   ✅ Pass: Balances re-calculated and inversion complete.\n")

if __name__ == "__main__":
    run_production_api_tests()