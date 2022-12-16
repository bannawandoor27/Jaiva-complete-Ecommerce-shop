from django.urls import path
from . import views
urlpatterns = [
      path("coupon/",views.coupon,name='coupon'),
]