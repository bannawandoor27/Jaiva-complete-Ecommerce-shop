from django.contrib import admin
from .models import Product,Variation, Wishlist, WishlistItem,ContactMessage

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
  list_display = ('product_name', 'price', 'stock', 'category', 'sub_category', 'modified_date', 'is_featured', 'is_available')
  prepopulated_fields = {'slug':('product_name',)}

class VariationAdmin(admin.ModelAdmin):
  list_display = ('product','variation_category','variation_value','is_active')
  list_editable = ('is_active',)
  list_filter = ('product','variation_category','variation_value',)

class WishlistAdmin(admin.ModelAdmin):
  list_display = ('wishlist_id', 'date_added',)
  
class WishlistItemAdmin(admin.ModelAdmin):
  list_display = ('product', 'wishlist',)
  
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem, WishlistItemAdmin)

admin.site.register(Variation, VariationAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ContactMessage)