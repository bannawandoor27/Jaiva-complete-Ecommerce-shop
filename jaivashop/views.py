from django.shortcuts import render
from category.models import *
from .models import *
# Create your views here.
def home(request):
  featured_categories = Sub_Category.objects.all().filter(is_featured=True)[:5]
  featured_products = Product.objects.all().filter(is_featured=True)[:8]
  all_categories = Category.objects.all()
  
  context = {
    'featured_categories': featured_categories,
    'featured_products'  : featured_products,
    'categories'         : all_categories
  }
  
  return render(request, 'home.html', context)
def shop(request):
    return render(request,'shop')

def product_details(request):
    pass