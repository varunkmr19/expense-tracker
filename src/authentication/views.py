import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from validate_email import validate_email


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        print(email)
        if not validate_email(email):
            return JsonResponse({'error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email alreday in use.'}, status=409)
        return JsonResponse({'success': 'Email is valid.'}, status=200)


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

    def post(self, request):
        # save form values to render back to the user in case of errors
        context = {
            'field_values': request.POST
        }
        # Get user data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # validate user data
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'password must be greated than 6.')
                    return render(request, 'authentication/register.html', context)
                # create and save user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.save()
                messages.success(
                    request, 'Account created successfully. Please, login to continue.')
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')
