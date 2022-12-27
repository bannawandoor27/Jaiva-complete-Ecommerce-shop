from django.db import models
from django.urls import reverse
from category.models import Category, Sub_Category
from accounts.models import Account
# Create your models here.

class Product(models.Model):
  
  UNIT = (('Kg', 'Kg'),
          ('litre', 'litre'),
          ('pack', 'pack'),
          ('bottle', 'bottle'),
          )
  product_name = models.CharField(max_length=200, unique=True)
  slug = models.SlugField(max_length=255, unique=True)
  description = models.TextField(max_length=500, blank=True)
  price = models.IntegerField()
  product_offer = models.IntegerField(default = 0)
  unit = models.CharField(max_length=50,choices=UNIT,default='Kg')
  image_1 = models.ImageField(upload_to='photos/products', blank=False)
  image_2 = models.ImageField(upload_to='photos/products', blank=True)
  image_3 = models.ImageField(upload_to='photos/products', blank=True)
  image_4 = models.ImageField(upload_to='photos/products', blank=True)
  stock = models.IntegerField()
  is_available = models.BooleanField(default=True)
  is_featured = models.BooleanField(default=False)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  
  def get_url(self):
    return reverse('product_details', args=[self.category.slug, self.sub_category.slug, self.slug])
  
 
  
  def __str__(self):
    return self.product_name
  
  def offer_price(self):
    product_offer = int(self.price) - int(self.price) * int(self.product_offer) /100 
    category_offer = int(self.price) - int(self.price) * int(self.category.category_offer)/100
    if product_offer == int(self.price) and category_offer == int(self.price):
        return self.price
    if product_offer <= category_offer:
        return int(product_offer)
    else:
        return category_offer



class VariationManager(models.Manager):
  def weights(self):
    return super(VariationManager, self).filter(variation_category='weight', is_active=True)
  
variation_category_choice =  (
    ('weight','weight'),
)

class Variation(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  variation_category = models.CharField(max_length=100, choices=variation_category_choice)
  variation_value = models.CharField(max_length=100)
  is_active = models.BooleanField(default=True)
  created_date = models.DateTimeField(auto_now=True)

  objects = VariationManager()


  def __str__(self):
    return self.variation_value


class Wishlist(models.Model):
  wishlist_id = models.CharField(max_length=250, blank=True)
  date_added = models.DateField(auto_now_add=True)
  
  def __str__(self):
    return self.wishlist_id

class WishlistItem(models.Model):
  user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE,null=True)
  is_active = models.BooleanField(default=True)
  cart_status = models.BooleanField(default=False)
  def __unicode__(self):
    return self.product


class ContactMessage(models.Model):
  user_name = models.CharField(max_length=100)
  email = models.EmailField()
  message = models.TextField(default='hai jaiva ')
  def __str__(self):
    return self.user_name