from django.contrib.auth.models import User
from django.db import models
from .utils import category_icon_directory_path


class Category(models.Model):
  '''Model to store various expense categories'''
  name = models.CharField(max_length=120)
  icon = models.FileField(upload_to=category_icon_directory_path)

  class Meta():
    verbose_name_plural = "categories"

  def __str__(self) -> str:
    return self.name

class Transaction(models.Model):
  ''' Model to track all exenses '''
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
  amount = models.DecimalField(max_digits=12, decimal_places=2) # max upto 1 billion, sorry Elon :D
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='transactions', null=True)
  description = models.CharField(max_length=255, null=True, blank=True)
  is_credited = models.BooleanField(default=False) # Credit: Earned / Debit: Spent
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self) -> str:
      return f'{self.user.username} - {self.amount}'
