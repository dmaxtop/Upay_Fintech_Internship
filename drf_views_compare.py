from rest_framework.views import APIView
from rest_framework.generics import  ListCreateAPIView
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import  get_object_or_404
from models import Transaction
from serializers import TransactionSerializer

# Approach 1: APIView (The Explicit / Low-Level Approach)

class TransactionAPIView(APIView):
    """
    - Pros: Complete control over HTTP methods.GET or POST is easily rtractable.
    - Cons: boilerplate, manually handling querysets,
        serialization, validation, and HTTP status codes all needs to be manual or using template.
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


# Approach 2: GenericAPIView + Mixins (The Semi-Automated Approach)

class TransactionGenericAPIView(ListCreateAPIView):
    """
    ListCreateApi View Combines GenericAPIView, ListModelMixin, and CreateModelMixin automatically.
    """
    """
    - Pros: Reduces boilerplate , standard actions (listing, creating) are reusable Mixins. 
    - Cons: Code starts becoming declarative ("magic"). 
            queries like `self.list()` maps to a GET request(and etc)
            handles serialization automatically.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        # self.list comes from ListModelMixin
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # self.create comes from CreateModelMixin
        return self.create(request, *args, **kwargs)


# Approach 3: ModelViewSet (The Rapid, Standardized Approach)

class TransactionViewSet(viewsets.ModelViewSet):
    """
    - Pros: Zero boilerplate for standard CRUD.    
            .list(), .create(), .retrieve(), .update(), and .destroy() is a single class. 
            Pairs with Routers and automatically generates URL configurations.
    
    - Cons: Hard customization behavior (needs to override hooks). 
            hides configuration behind abstraction , not ideal for non-standard APIs.
            Debugging medium hard.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


