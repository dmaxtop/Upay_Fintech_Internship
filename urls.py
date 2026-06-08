# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .drf_views_comparison import (
    TransactionAPIView, 
    TransactionGenericAPIView, 
    TransactionViewSet
)

# Set up the router specifically for Approach 3
router = DefaultRouter()
router.register(r'tx-viewset', TransactionViewSet, basename='tx-viewset')

urlpatterns = [
    # Approach 1: Low-level APIView
    path('tx-apiview/', TransactionAPIView.as_view(), name='tx-apiview'),
    
    # Approach 2: GenericAPIView + Mixins
    path('tx-generic/', TransactionGenericAPIView.as_view(), name='tx-generic'),
    
    # Approach 3: ModelViewSet managed by Router
    path('', include(router.urls)),
]