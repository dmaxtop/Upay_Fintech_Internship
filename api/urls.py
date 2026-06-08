# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 1. Import Live Production ViewSets (Tasks 2 & 3)
from .views import AccountViewSet, TransactionViewSet

# 2. Import DRF Structural Evolution Comparison Views (Task 1)
from .drf_views_compare import (
    TransactionAPIView,
    TransactionGenericAPIView,
    TransactionViewSet as CompareTransactionViewSet  # Aliased to prevent clashing with production views
)

# 3. Import Traditional Django Comparison Views (Task 0)
from .django_views_compare import (
    AccountLowLevelView,
    AccountDashboardView,
    AccountListView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView
)

# Initialize the router to auto-generate standard CRUD resource paths
router = DefaultRouter()

# Register Live Production REST API Endpoints (Task 2 & 3)
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')

# Register DRF Approach 3 (ModelViewSet) with a distinctive prefix path to avoid resource clashing
router.register(r'compare/drf/viewset', CompareTransactionViewSet, basename='compare-tx-viewset')

urlpatterns = [
    # Router endpoints (Production paths + DRF Compare ViewSet path)
    path('', include(router.urls)),

    # =====================================================================
    # Task 1: DRF Comparison View Endpoints (Manual APIViews)
    # =====================================================================
    path('compare/drf/apiview/', TransactionAPIView.as_view(), name='compare-tx-apiview'),
    path('compare/drf/generic/', TransactionGenericAPIView.as_view(), name='compare-tx-generic'),

    # =====================================================================
    # Task 0: Traditional Django View Comparison Endpoints
    # =====================================================================
    path('compare/django/low-level/', AccountLowLevelView.as_view(), name='compare-django-lowlevel'),
    path('compare/django/dashboard/', AccountDashboardView.as_view(), name='compare-django-dashboard'),
    path('compare/django/list/', AccountListView.as_view(), name='compare-django-list'),
    path('compare/django/create/', AccountCreateView.as_view(), name='compare-django-create'),
    path('compare/django/update/<int:pk>/', AccountUpdateView.as_view(), name='compare-django-update'),
    path('compare/django/delete/<int:pk>/', AccountDeleteView.as_view(), name='compare-django-delete'),
]