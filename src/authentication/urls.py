from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import EmailValidationView, LoginView, LogoutView, RegistrationView, UsernameValidationView


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegistrationView.as_view(), name='register'),
    path('logout', LogoutView, name='logout'),
    path('validate_username', csrf_exempt(UsernameValidationView.as_view()),
         name='validate_username'),
    path('validate_email', csrf_exempt(EmailValidationView.as_view()),
         name='validate_email')
]
