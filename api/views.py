from unicodedata import category
from urllib import request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from expense_app.models import Category, SubCategory, Transaction
from api.serializers import CategorySerializer, TransactionSerializer


class ListCategories(APIView):
  """
  View to list all categories and it's related subcategories
  """
  def get(self, request, format=None):
    """
    Return a list of all categories
    """
    categories = Category.objects.prefetch_related('subcategory').all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ListTransactions(APIView):
  """
  View to list all transactions
  """
  def get(self, request, format=None):
    """
    Return a list of all transactions made by the user
    """
    transactions = Transaction.objects.filter(user=request.user)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    """
    Save a transaction against the logged in user
    """
    data = request.data
    try:
      sub_category = SubCategory.objects.get(pk=data.get('category'))
      data.pop('category')
      transaction = Transaction.objects.create(user=request.user, category=sub_category, **data)
      serializer = TransactionSerializer(transaction)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    except SubCategory.DoesNotExist:
      return Response(exception=True, status=status.HTTP_404_NOT_FOUND)
    
