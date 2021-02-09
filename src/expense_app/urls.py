from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegistrationView.as_view(), name='register'),
    path('logout', views.logout_view, name='logout'),
    path('home', views.home_view, name='home'),
    path('bill/<int:pk>', views.bill_detail_view, name='bill_detail'),
    path('bill/create', views.create_bill, name='create_bill'),
    path('bill/update/<int:pk>', views.edit_bill, name='edit_bill'),
    path('bill/delete/<int:pk>', views.delete_bill, name='delete_bill'),
]