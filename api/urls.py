from django.urls import path
from api import views

urlpatterns = [
  path('categories/', views.ListCategories.as_view()),
  path('transactions/', views.ListTransactions.as_view()),
  path('transactions/<int:pk>', views.TransactionDetail.as_view()),
]