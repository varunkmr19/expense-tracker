from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  pass

class Category(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name;

class Bill(models.Model):
  added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='bill')
  description = models.CharField(max_length=250)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateField(auto_now_add=True)

  def __str__(self):
    return f'{self.category} - {self.amount}'