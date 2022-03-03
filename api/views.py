from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from expense_app.models import Category, SubCategory, Transaction
from api.serializers import CategorySerializer, TransactionSerializer
from api.response import response


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
    return response(status=status.HTTP_200_OK, message="Success", data=serializer.data)


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
    return response(status=status.HTTP_200_OK, message="Success", data=serializer.data)

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
      return response(status=status.HTTP_201_CREATED, message="Success", data=serializer.data)
    except SubCategory.DoesNotExist:
      return response(status=status.HTTP_404_NOT_FOUND, message="Category not found")
    
