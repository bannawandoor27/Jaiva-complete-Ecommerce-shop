from django.urls import path
from . import views

urlpatterns = [
  path('home/', views.home, name='home'),
  path('shop/', views.shop, name='shop'),
  path('shop/<slug:category_slug>/', views.shop, name='products_by_category'),
  path('shop/<slug:category_slug>/<slug:sub_category_slug>/', views.shop, name='products_by_sub_category'),
  path('shop/<slug:category_slug>/<slug:sub_category_slug>/<slug:product_slug>/', views.product_details, name='product_details'),
  path('shop_filter/', views.shop, name='shop_filter'),
  path('search/', views.search, name='search'),
  path('wishlist/',views.wishlist,name='wishlist'),
  path('add_wishlist/<int:product_id>/',views.add_wishlist,name='add_wishlist'),
  path('remove_wishlist_item/<int:product_id>/<int:wishlist_item_id>/', views.remove_wishlist_item, name='remove_wishlist_item'),
  path('contact_us',views.contact_us,name='contact_us')
]