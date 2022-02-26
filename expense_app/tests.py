import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User
from expense_app.models import Category, Transaction

# Create your tests here.
class CategoryTestCase(TestCase):
  def setUp(self) -> None:
      self.category1 = Category.objects.create(name="Grocery", icon=SimpleUploadedFile('grocery.png', b'file content'))
      self.category2 =Category.objects.create(name="Rent", icon=SimpleUploadedFile('rent.png', b'file content'))
      

  def test_category_create_method(self) -> None:
    ''' Grocery name field must be equal with the return value of __str__() method. '''
    grocery = Category.objects.get(name='Grocery')
    rent = Category.objects.get(name='Rent')
    self.assertEqual(grocery.__str__(), 'Grocery')
    self.assertEqual(rent.__str__(), 'Rent')
  
  def tearDown(self) -> None:
      os.remove(self.category1.icon.path)
      os.remove(self.category2.icon.path)

class TranscationTestCase(TestCase):
  def setUp(self) -> None:
      self.dummy_user = User.objects.create_user(username='dummy_user', password='dummy@pass123')
      self.category = Category.objects.create(name="Grocery", icon=SimpleUploadedFile('grocery.png', b'file content'))
      Transaction.objects.create(
        user=self.dummy_user,
        amount=50,
        category=self.category,
        description='veggies'
      )
  
  def test_transaction_create_method(self) -> None:
    grocery_bill = Transaction.objects.get(description='veggies')
    self.assertEqual(grocery_bill.__str__(), 'dummy_user - 50.00')

  def tearDown(self) -> None:
      os.remove(self.category.icon.path)