# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import your initial architectural comparison views
from api.drf_views_compare import (
    TransactionAPIView, 
    TransactionGenericAPIView
)



from api.drf_views_custom_methods import AccountViewSet, TransactionViewSet

# Initialize the single central router
router = DefaultRouter()

# Task 2: Wire up full CRUD endpoints for Account and Transaction
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    # --- Architectural Comparison Paths (From Steps 1 & 2) ---
    path('tx-apiview/', TransactionAPIView.as_view(), name='tx-apiview'),
    path('tx-generic/', TransactionGenericAPIView.as_view(), name='tx-generic'),
    
    # --- Production API Paths (From Steps 3 & 4) ---
    # automatically includes paths for standard CRUD as well as custom
    # @action methods: /api/accounts/{id}/freeze/, /api/accounts/{id}/statement/, etc.
    path('api/', include(router.urls)),
]