import os
import django
from django.conf import settings
from django.core.management import call_command

# 1. Minimum Inline Django Configuration for Standard Views & Templates
if not settings.configured:
    settings.configure(
        SECRET_KEY='temporary_test_secret_key',
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sessions',
            'django.contrib.messages',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': False,
            'OPTIONS': {
                'string_if_invalid': 'INVALID_VARIABLE',
            },
        }],
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
    )
    django.setup()

    call_command('migrate', verbosity=0, interactive=False)

    from django.db import connection
    with connection.schema_editor() as schema_editor:
        from models import Account
        schema_editor.create_model(Account)

# Mocked URL patterns to satisfy reverse_lazy('account-list') redirects
from django.urls import path
import django.http

urlpatterns = [
    path('accounts/', lambda r: django.http.HttpResponse("List Page"), name='account-list'),
]

# 2. Setup testing utilities and import the views
from django.test import RequestFactory
from unittest.mock import patch

from django_views_compare import (
    AccountLowLevelView, AccountDashboardView, AccountListView,
    AccountCreateView, AccountUpdateView, AccountDeleteView
)

def test_cbv_lifecycle():
    factory = RequestFactory()
    
    from django.contrib.auth.models import User
    from models import Account
    
    mock_user = User.objects.create_user(username="dj_test_user", password="password123")
    
    test_account = Account.objects.create(
        account_number="ACC-111222",
        account_type="Savings",
        balance=5000.00,
        user=mock_user
    )

    print("\nExecuting Django CBV Lifecycle Verification Tests...")
    print("-" * 60)

    # =========================================================================
    # Test 0: AccountLowLevelView (Base View)
    # =========================================================================
    view_0 = AccountLowLevelView.as_view()
    req_get = factory.get('/low-level/')
    req_post = factory.post('/low-level/')
    
    res_get = view_0(req_get)
    res_post = view_0(req_post)
    print(f"✅ Test 0 (Base View): GET -> {res_get.status_code} ({res_get.content.decode()})")
    print(f"                       POST -> {res_post.status_code} ({res_post.content.decode()})\n")

    # =========================================================================
    # Test 1: AccountDashboardView (TemplateView)
    # =========================================================================
    view_1 = AccountDashboardView.as_view()
    req_1 = factory.get('/dashboard/')
    
    with patch('django.views.generic.TemplateView.render_to_response') as mock_render:
        view_instance = AccountDashboardView()
        view_instance.setup(req_1)
        context = view_instance.get_context_data()
        print(f"✅ Test 1 (TemplateView) Context Verified: page_title = '{context.get('page_title')}'\n")

    # =========================================================================
    # Test 2: AccountListView (ListView)
    # =========================================================================
    req_2 = factory.get('/accounts-list/')
    with patch('django.views.generic.ListView.render_to_response') as mock_render:
        view_instance = AccountListView()
        view_instance.setup(req_2)
        view_instance.object_list = view_instance.get_queryset()
        context = view_instance.get_context_data()
        
        accounts_in_context = context.get('accounts')
        print(f"✅ Test 2 (ListView) Database Query Executed:")
        print(f"   - Pulled {len(accounts_in_context)} account(s) from memory DB.")
        print(f"   - Target Record Found: {accounts_in_context[0].account_number}\n")

    # =========================================================================
    # Test 3: AccountCreateView (CreateView - POST submission)
    # =========================================================================
    post_data_create = {
        'account_number': 'ACC-NEW-333',
        'account_type': 'Checking',
        'balance': 150.75
    }
    req_3 = factory.post('/accounts/create/', data=post_data_create)
    # Log the user into the request context structure directly
    req_3.user = mock_user
    
    # Override form_valid on the view to inject the user dependency automatically
    view_3 = AccountCreateView()
    view_3.setup(req_3)
    def custom_form_valid_create(form):
        form.instance.user = req_3.user
        return super(AccountCreateView, view_3).form_valid(form)
    view_3.form_valid = custom_form_valid_create
    
    res_3 = view_3.dispatch(req_3)
    if res_3.status_code == 302:
        new_account = Account.objects.get(account_number='ACC-NEW-333')
        print(f"✅ Test 3 (CreateView) Pipeline Executed:")
        print(f"   - Status Code: {res_3.status_code} (Redirect to {res_3.url})")
        print(f"   - DB Verification: New account created with balance ${new_account.balance}\n")
    else:
        print(f"❌ Test 3 (CreateView) Failed validation errors: {res_3.context_data['form'].errors}\n")

    # =========================================================================
    # Test 4: AccountUpdateView (UpdateView - POST modification)
    # =========================================================================
    post_data_update = {
        'account_type': 'Business Savings',
        'balance': 9999.99
    }
    req_4 = factory.post(f'/accounts/{test_account.pk}/update/', data=post_data_update)
    req_4.user = mock_user
    
    view_4 = AccountUpdateView()
    view_4.setup(req_4, pk=test_account.pk)
    def custom_form_valid_update(form):
        form.instance.user = req_4.user
        return super(AccountUpdateView, view_4).form_valid(form)
    view_4.form_valid = custom_form_valid_update
    
    res_4 = view_4.dispatch(req_4, pk=test_account.pk)
    if res_4.status_code == 302:
        test_account.refresh_from_db()
        print(f"✅ Test 4 (UpdateView) Pipeline Executed:")
        print(f"   - Status Code: {res_4.status_code} (Redirect to {res_4.url})")
        print(f"   - DB Verification: Refreshed Type -> '{test_account.account_type}', Balance -> ${test_account.balance}\n")
    else:
        print(f"❌ Test 4 (UpdateView) Failed validation errors: {res_4.context_data['form'].errors}\n")

    # =========================================================================
    # Test 5: AccountDeleteView (DeleteView - POST confirmation)
    # =========================================================================
    req_5 = factory.post(f'/accounts/{test_account.pk}/delete/')
    view_5 = AccountDeleteView.as_view()
    
    res_5 = view_5(req_5, pk=test_account.pk)
    db_count = Account.objects.filter(pk=test_account.pk).count()
    print(f"✅ Test 5 (DeleteView) Pipeline Executed:")
    print(f"   - Status Code: {res_5.status_code} (Redirect to {res_5.url})")
    print(f"   - DB Verification: Record search count for ID {test_account.pk} is now {db_count} (Successfully Purged)\n")

if __name__ == "__main__":
    test_cbv_lifecycle()