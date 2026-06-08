# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, TransactionViewSet


from .drf_views_compare import (
    TransactionAPIView,
    TransactionGenericAPIView,
    TransactionViewSet as CompareTransactionViewSet  # Renamed with alias to avoid collision
)

from .django_views_compare import AccountLowLevelView

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]