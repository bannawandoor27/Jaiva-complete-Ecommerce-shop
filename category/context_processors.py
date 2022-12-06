from .models import Category, Sub_Category

def category_links(request):
  cat_links = Category.objects.all().order_by('-category_offer')
  return dict(cat_links=cat_links)

def sub_category_links(request):
  sub_cat_links = Sub_Category.objects.all()
  return dict(sub_cat_links=sub_cat_links)