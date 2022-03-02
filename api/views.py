from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from expense_app.models import Category
from api.serializers import CategorySerializer


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