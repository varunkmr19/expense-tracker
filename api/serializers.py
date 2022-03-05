from dataclasses import fields
from email.policy import default
from rest_framework import serializers
from expense_app.models import Category, SubCategory, Transaction


class SubCategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = SubCategory
    fields = ('id', 'name', 'icon')


class CategorySerializer(serializers.ModelSerializer):
  subcategory = SubCategorySerializer(many=True, read_only=True)
  class Meta:
    model = Category
    fields = ('id', 'name', 'icon', 'subcategory')

class TransactionSerializer(serializers.ModelSerializer):
  user = serializers.HiddenField(default
  =serializers.CurrentUserDefault())
  category  = SubCategorySerializer()
  class Meta:
    model = Transaction
    fields = '__all__'