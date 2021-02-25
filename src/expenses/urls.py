from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.index_view, name='expenses'),
    path('addexpenses', views.add_expenses, name='add_expenses')
]
