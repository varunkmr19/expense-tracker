from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.index_view, name='expenses'),
    path('addexpenses', views.add_expenses, name='add_expenses'),
    path('editexpense/<int:expense_id>',
         views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:pk>',
         views.DeleteExpense.as_view(), name='delete_expense')
]
