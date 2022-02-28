from django.shortcuts import render
from expense_app.models import Category, SubCategory

# Create your views here.
def index_view(request):
  categories = Category.objects.prefetch_related('child').all()
  return render(request, 'expense_app/index.html', context={
    'categories': categories
  })