from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegistrationView.as_view(), name='register'),
    path('logout', views.logout_view, name='logout'),
    path('home', views.BillListView.as_view(), name='home'),
    path('bill/<int:pk>', views.BillDetailView.as_view(), name='bill'),
    path('bill/create', views.BillCreateView.as_view(), name='create_bill'),
    path('bill/update/<int:pk>', views.BillUpdateView.as_view(), name='update_bill')
]