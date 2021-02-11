from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import BillForm
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

@login_required
def home_view(request):
  # get bills
  bills = Bill.objects.filter(added_by=request.user).all()
  total_amount = 0
  for bill in bills:
    total_amount += bill.amount

  bill_per_share = total_amount/4

  return render(request, 'expense_app/home.html', {
    'bills': bills,
    'total': total_amount,
    'share': bill_per_share
  })

@login_required
def create_bill(request):
  if request.method == 'POST':
    form = BillForm(request.POST)
    if form.is_valid():
      category = form.cleaned_data['category']
      description = form.cleaned_data['description']
      amount = form.cleaned_data['amount']
      new_bill = Bill.objects.create(
        added_by=request.user,
        category=category,
        description=description,
        amount=amount
      )
      new_bill.save()
    return HttpResponseRedirect(reverse('home'))
  else:
    form = BillForm()
    return render(request, 'expense_app/create_bill.html', {
      'form':form
    })

@login_required
def bill_detail_view(request, pk):
  bill = get_object_or_404(Bill, pk=pk)
  return render(request, 'expense_app/bill_detail.html', {
    'bill': bill
  })

@login_required
def edit_bill(request, pk):
  try:
    bill = Bill.objects.get(added_by=request.user, pk=pk)
  except Bill.DoesNotExist:
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

  form = BillForm(request.POST or None, instance=bill)

  if form.is_valid():
    bill.category = form.cleaned_data['category']
    bill.description = form.cleaned_data['description']
    bill.amount = form.cleaned_data['amount']
    bill.save()

    return HttpResponseRedirect(f'/bill/{pk}')
  
  return render(request, 'expense_app/create_bill.html', {
    'form': form
  })

@login_required
def delete_bill(request, pk):
  bill = get_object_or_404(Bill, pk=pk)
  bill.delete()
  return HttpResponseRedirect(reverse('home'))

