import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'error': 'Username should only contain alphanumeric characters.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": 'username already taken.'}, status=409)
        return JsonResponse({'success': 'Username is valid.'})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
