from django import contrib
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Expense
from . import utils

# Create your views here.


@login_required(login_url='/auth/login')
def index_view(request):
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    context = {
        'expenses': expenses
    }
    return render(request, 'expenses/index.html', context)


def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'POST':
        # get user input
        amount = request.POST['amount']
        category = request.POST['category']
        description = request.POST['description']
        date = request.POST['date']

        # validate user inputs
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expenses.html', context)
        if utils.validate_amount(amount) == False:
            messages.error(request, 'Only Numbers are allowed')
            return render(request, 'expenses/add_expenses.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expenses.html', context)

        Expense.objects.create(amount=amount, date=date, category=category,
                               description=description, owner=request.user)

        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')

    return render(request, 'expenses/add_expenses.html', context)
