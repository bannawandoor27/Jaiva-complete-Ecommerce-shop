from .models import Product
from .models import Wishlist,WishlistItem
from .views import _wishlist_id
from .models import ContactMessage

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

def wishlist_counter(request):
    wishlist_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            wishlist = Wishlist.objects.filter(wishlist_id=_wishlist_id(request))
            if request.user.is_authenticated:
                wishlist_items = WishlistItem.objects.all().filter(user=request.user)
            else:
                wishlist_items = WishlistItem.objects.all().filter(wishlist=wishlist[:1])
            for wishlist_item in wishlist_items:
                wishlist_count += 1
        except Wishlist.DoesNotExist:
            wishlist_count = 0
    return dict(wishlist_count=wishlist_count)

def all_messages (request):
  latest_messages = ContactMessage.objects.all()[:3]
  return dict(all_messages=latest_messages)