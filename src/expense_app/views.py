from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.views import View, generic
from .models import User, Bill

# Create your views here.
class LoginView(View):
  def get(self, request):
    return render(request, 'expense_app/login.html')

  def post(self, request):
    # Attempt to sign user in
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse('index'))
    else:
      return render(request, 'expense_app/login.html', {
        'error': 'Invalid username and/or password.'
      })

def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse('index'))

class RegistrationView(View):
  def get(self, request):
    return render(request, 'expense_app/register.html')

  def post(self, request):
    username = request.POST['username']
    email = request.POST['email']

    # Ensure password matches confirmation
    password = request.POST['password']
    confirmation = request.POST['confirmation']
    if password != confirmation:
      return render(request, 'expense_app/register.html', {
        'error': 'Passwords must match.'
      })
    
    # Attempt to create new user
    try:
      user = User.objects.create_user(username, email, password)
      user.save()
    except IntegrityError:
      return render(request, 'expense_app/register.html', {
        'error': 'Username already taken.'
      })
    login(request, user)
    return HttpResponseRedirect(reverse('index'))


class IndexView(View):
  def get(self, request):
    return render(request, 'expense_app/index.html')

class BillListView(generic.list.ListView):
  # List bills of active user
  model = Bill
  context_object_name = 'bills'
  template_name = 'expense_app/home.html'

  # def get_queryset(self):
  #   queryset = Bill.objects.filter(added_by=self.request.user)

class BillDetailView(generic.detail.DetailView):
  model = Bill
  context_object_name = 'bill'
  template_name = 'expense_app/bill_detail.html'

