from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import RegistrationView, UsernameValidationView


urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('validate_username', csrf_exempt(UsernameValidationView.as_view()),
         name='validate_username')
]
