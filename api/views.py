from unicodedata import category
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from expense_app.models import Category, SubCategory, Transaction
from api.serializers import CategorySerializer, SubCategorySerializer, TransactionSerializer
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
    

class TransactionDetail(APIView):
  """
  Retrieve, update or delete a transaction instance.
  """
  def get_object(self, pk):
    try:
      return Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
      return response(status=status.HTTP_404_NOT_FOUND, message="Transaction not found")
  
  def get(self, request, pk, format=None):
    transaction = self.get_object(pk)
    serializer = TransactionSerializer(transaction)
    return response(status=status.HTTP_200_OK, message='success', data=serializer.data)

  def put(self, request, pk, format=None):
    data = request.data
    transaction = self.get_object(pk)
    try:
      category = SubCategory.objects.get(pk=data.get('category'))
      transaction = Transaction.objects.get(pk=data.get('id'))

      transaction.amount = data.get('amount')
      transaction.description = data.get('description')
      transaction.category = category
      transaction.is_credit = data.get('is_credit')
      transaction.save()
      serializer = TransactionSerializer(transaction)
    except SubCategory.DoesNotExist:
      return response(status=status.HTTP_400_BAD_REQUEST, message="Category not found: please check the id")
    except Transaction.DoesNotExist:
      return response(status=status.HTTP_400_BAD_REQUEST, message="Transaction not found: please check the id")
    return response(status=status.HTTP_200_OK, message="updated successfully", data=serializer.data)

  def delete(self, request, pk, format=None):
    transaction = self.get_object(pk)
    transaction.delete()
    return response(status=status.HTTP_204_NO_CONTENT, message='deleted successfully')
