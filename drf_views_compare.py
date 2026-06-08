from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_buffer, get_object_or_404
from .models import Transaction
from .serializers import TransactionSerializer
# =====================================================================
# Approach 1: APIView (The Explicit / Low-Level Approach)
# =====================================================================
class TransactionAPIView(APIView):
    """
    TRADEOFFS:
    - Pros: Complete, explicit control over HTTP methods. You can see 
            exactly what happens on GET or POST. No magic.
    - Cons: High amount of boilerplate. You must manually handle querysets,
            serialization, validation, serialization errors, and HTTP status codes.
    """
    def get(self, request, format=None):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)