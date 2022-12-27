from django.shortcuts import get_object_or_404, redirect, render
from carts.models import CartItem,Cart
from carts.views import _cart_id
from category.models import *
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from jaivashop.models import Category, Product, Sub_Category
from django.core.exceptions import ObjectDoesNotExist
from jaivashop.models import ContactMessage
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
def shop(request, category_slug=None, sub_category_slug=None):
  categories_shop= None
  subCategories_shop = None
  products = None
  off_products = Product.objects.filter(product_offer__gt=0)
    
  if sub_category_slug != None:
    subCategories_shop = get_object_or_404(Sub_Category, slug=sub_category_slug)
    products = Product.objects.all().filter(sub_category=subCategories_shop, is_available=True)
    product_count = products.count()
    
  elif category_slug != None:
    categories_shop = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.all().filter(category=categories_shop, is_available=True)
    print(categories_shop)
    product_count = products.count()
        
  else:
    categories_shop = Category.objects.all()
    subCategories_shop = Sub_Category.objects.all()
    products = Product.objects.all().filter(is_available=True).order_by('product_name')
    product_count = products.count()
    
  if request.method == 'POST':
    min = request.POST['minamount']
    max = request.POST['maxamount']
    min_price = min.split('₹')[1]
    max_price = max.split('₹')[1]
    products = Product.objects.all().filter(Q(price__gte=min_price),Q(price__lte=max_price),is_available=True).order_by('price')
    product_count = products.count()
    
  
  paginator = Paginator(products, 9)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
    
  context = {
    'categories_shop':categories_shop,
    'subCategories_shop':subCategories_shop,
    'products':page_obj,
    'off_products':off_products,
    'product_count':product_count
  }
  return render(request, 'jaivashop/shop.html', context)

def product_details(request, category_slug, sub_category_slug, product_slug):
  categories = Category.objects.all()
  
  try:
    product = Product.objects.get(category__slug=category_slug, sub_category__slug=sub_category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()    
    related_products = Product.objects.filter(sub_category__slug=sub_category_slug)[:4]
    
  except Exception as e:
    raise e

  context = {
    'categories':categories,
    'product':product,
    "related_products":related_products,
    # "in_cart":in_cart,
  }
  return render(request, 'jaivashop/product_details.html', context)

def price_change(request):
  var_value = request.GET['var_value']
  pro_id = request.GET['pid']
  product = Product.objects.get(id=pro_id)
  price = product.offer_price()
  x = var_value.split()
  var_value = int(x[0])
  pro_price = price * var_value
  return JsonResponse(
          {'success': True,
           'pro_price':pro_price,
           },
          safe=False
        )

def search(request):
  if request.method == 'GET':
    keyword = request.GET['keyword']
    if keyword:
      products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
      product_count = products.count()
      
  paginator = Paginator(products, 9)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
      
  context = {
    'products':page_obj,
    'product_count':product_count,
  }
  return render(request, 'jaivashop/shop.html', context)


def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist

def add_wishlist(request,product_id):
  product = Product.objects.get(id=product_id)

  try:
    wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
  except Wishlist.DoesNotExist:
    wishlist =  Wishlist.objects.create(
      wishlist_id=_wishlist_id(request)
    )
    wishlist.save()

  try:
      wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist)
  except WishlistItem.DoesNotExist:
      wishlist_item = WishlistItem.objects.create(
            product  = product,
            wishlist = wishlist,
        )
      wishlist_item.save()
  if request.user.is_authenticated:
    wishlist_item.user = request.user
    wishlist_item.save()

  return redirect('wishlist')




def wishlist(request,wishlist_items=None):

    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist,is_active=True)
                
    except ObjectDoesNotExist:
        pass

    context = {
        'items' : wishlist_items
    }
    
    return render(request,'jaivashop/wishlist.html',context)

def remove_wishlist_item(request, product_id, wishlist_item_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        
        if request.user.is_authenticated:
            wishlist_item = WishlistItem.objects.get(product=product, user=request.user, id=wishlist_item_id)
            
        else:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist, id=wishlist_item_id)
        wishlist_item.delete()
    except:
        pass
    
    return redirect('wishlist')



def contact_us(request):
  if request.method == 'POST':
    
  return render(request,'contact.html')

