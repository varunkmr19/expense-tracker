from django.core import exceptions
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from rest_framework import serializers
from expense_app.models import Category, SubCategory, Transaction


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'password')
    write_only_fields = ('password',)
    read_only_fields = ('id',)

  def validate(self, data):
      user = User(**data)
      password = data.get('password')

      errors = dict()
      try:
        # validate password against the defined validators in settings.py
        password_validation.validate_password(password=password, user=user)
      except exceptions.ValidationError as e:
        errors['password'] = list(e.messages)
      if errors:
        raise serializers.ValidationError(errors)
      return super(UserSerializer, self).validate(data)

  def create(self, validated_data):
    instance = User.objects.create(
      username = validated_data.get('username'),
    )
    # hash password and add it to user instance
    instance.set_password(validated_data['password'])
    instance.save()

    return instance


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