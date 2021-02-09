from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegistrationView.as_view(), name='register'),
    path('logout', views.logout_view, name='logout')
]