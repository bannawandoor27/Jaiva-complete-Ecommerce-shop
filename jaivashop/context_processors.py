from .models import Product

def latest_products1(request):
  latest_products_1 = Product.objects.all().order_by('-created_date')[:3]
  return dict(latest_products_1=latest_products_1)

def latest_products2(request):
  latest_products_2 = Product.objects.all().order_by('-created_date')[3:6]
  return dict(latest_products_2=latest_products_2)

def home_made1(request):
  home_made = Product.objects.all().order_by('-product_offer')[:3]
  return dict(home_made1=home_made)

def home_made2(request):
  home_made = Product.objects.all().order_by('-product_offer')[3:6]
  return dict(home_made2=home_made)

def today_special1(request):
  today_special = Product.objects.all().order_by('stock')[:3]
  return dict(today_special1=today_special)

def today_special2(request):
  today_special = Product.objects.all().order_by('stock')[:3]
  return dict(today_specia21=today_special)
