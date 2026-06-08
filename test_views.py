import os
import django
from django.conf import settings
from django.core.management import call_command

# 1. Minimum Inline Django Configuration (with an in-memory database)
if not settings.configured:
    settings.configure(
        SECRET_KEY='temporary_test_secret_key',
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'rest_framework',
        ],
        # We give it an in-memory SQLite DB so ORM calls won't crash the script
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

    # Automatically construct the model tables in our virtual memory DB
    # This ensures Transaction.objects.all() actually finds an existing table!
    from django.db import connection
    with connection.schema_editor() as schema_editor:
        from models import Account, Transaction
        schema_editor.create_model(Account)
        schema_editor.create_model(Transaction)

# 2. Setup DRF test utilities and views
from rest_framework.test import APIRequestFactory
from drf_views_compare import TransactionAPIView, TransactionGenericAPIView

def test_view_lifecycle():
    factory = APIRequestFactory()
    
    # -------------------------------------------------------------------------
    # 0. Database Pre-population
    # -------------------------------------------------------------------------
    # Create a dummy Account in the in-memory database first.
    # If your Account model has other mandatory fields, define them here.
    from models import Account
    mock_account = Account.objects.create(account_number="ACC-MOCK-999")
    
    print("\nExecuting Explicit Verification Tests...")
    print("-" * 50)

    # =========================================================================
    # Test 1: Testing Approach 1 (APIView) GET Request (Initial Empty State)
    # =========================================================================
    view_1 = TransactionAPIView.as_view()
    request_1 = factory.get('/tx-apiview/')
    
    try:
        response_1 = view_1(request_1)
        print(f"✅ Approach 1 (APIView) GET Compiled & Executed.")
        print(f"   Status Code: {response_1.status_code}")
        print(f"   Data (Before POST): {response_1.data}\n")
    except Exception as e:
        print(f"❌ Approach 1 GET Failed unexpected error: {e}\n")

    # =========================================================================
    # Test 2: Testing Approach 2 (GenericAPIView) POST Request Routing
    # =========================================================================
    view_2 = TransactionGenericAPIView.as_view()
    
    # Passing the valid mock account ID clears the 400 validation hurdle!
    test_data = {
        "amount": "100.00",
        "account": mock_account.id
    } 
    request_2 = factory.post('/tx-generic/', data=test_data, format='json')
    
    try:
        response_2 = view_2(request_2)
        print(f"✅ Approach 2 (GenericAPIView) POST Compiled & Executed.")
        print(f"   Status Code: {response_2.status_code}")
        print(f"   Response Body (Created Data): {response_2.data}\n")
    except Exception as e:
        print(f"❌ Approach 2 POST Failed unexpected error: {e}\n")

    # =========================================================================
    # Test 3: Re-running Approach 1 (APIView) GET Request (Verification State)
    # =========================================================================
    try:
        response_3 = view_1(request_1)
        print(f"✅ Approach 1 (APIView) GET Re-Verification Executed.")
        print(f"   Status Code: {response_3.status_code}")
        print(f"   Data (After POST): {response_3.data}\n")
    except Exception as e:
        print(f"❌ Approach 1 Re-Verification Failed unexpected error: {e}\n")

if __name__ == "__main__":
    test_view_lifecycle()