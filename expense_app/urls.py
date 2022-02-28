from django.urls import path
from expense_app.views import index_view

urlpatterns = [
    path('', index_view, name='index'),
]