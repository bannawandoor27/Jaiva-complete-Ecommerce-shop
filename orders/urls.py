from django.urls import path
from . import views
urlpatterns = [
      path("coupon/",views.coupon,name='coupon'),
      path('place_order/', views.place_order, name='place_order'),
      path('payments/', views.payments, name='payments'),
      path('razorpay/', views.razorpay, name='razorpay'),
      
      path('payments_completed/',views.payments_completed,name = 'payments_completed'),
      
      path("cash_on_delivery/<int:id>/",views.cash_on_delivery,name='cash_on_delivery'),
      

]