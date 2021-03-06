from django.core import paginator
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Category, Expense
from . import utils

# Create your views here.


@login_required(login_url='/auth/login')
def index_view(request):
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'expenses': expenses,
        'page_obj': page_obj
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/auth/login')
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


@login_required(login_url='/auth/login')
def edit_expense(request, expense_id):
    category = Category.objects.all()
    expense = Expense.objects.get(pk=expense_id)
    context = {
        'expense': expense,
        'categories': category,
    }

    if request.method == 'POST':
        # get user inputs
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']

        # validate user inputs
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit_expense.html', context)

        # update expenses data
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated successfully')

        return redirect('expenses')

    return render(request, 'expenses/edit_expense.html', context)


class DeleteExpense(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Expense
    success_url = reverse_lazy('expenses')
    login_url = '/auth/login'
    success_message = 'Expense deleted successfully'
    template_name = 'expenses/delete_expense.html'
