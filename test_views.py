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
    
    print("\nExecuting Explicit Verification Tests...")
    print("-" * 50)

    # =========================================================================
    # Test 1: Testing Approach 1 (APIView) GET Request Execution
    # =========================================================================
    view_1 = TransactionAPIView.as_view()
    request_1 = factory.get('/tx-apiview/')
    
    try:
        response_1 = view_1(request_1)
        print(f"✅ Approach 1 (APIView) Compiled & Executed.")
        print(f"   Status Code: {response_1.status_code}")
        print(f"   Data: {response_1.data}\n")
    except Exception as e:
        print(f"❌ Approach 1 Failed unexpected error: {e}\n")

    # =========================================================================
    # Test 2: Testing Approach 2 (GenericAPIView) POST Request Routing
    # =========================================================================
    view_2 = TransactionGenericAPIView.as_view()
    
    # NOTE: If your Transaction model requires other fields, add them here 
    # to convert the status code from a 400 Bad Request to a 201 Created.
    test_data = {"amount": "100.00"} 
    request_2 = factory.post('/tx-generic/', data=test_data, format='json')
    
    try:
        response_2 = view_2(request_2)
        print(f"✅ Approach 2 (GenericAPIView) Compiled & Executed.")
        print(f"   Status Code: {response_2.status_code}")
        print(f"   Response Body/Errors: {response_2.data}\n")
    except Exception as e:
        print(f"❌ Approach 2 Failed unexpected error: {e}\n")

if __name__ == "__main__":
    test_view_lifecycle()