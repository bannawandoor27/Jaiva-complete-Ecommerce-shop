from django.urls import path
from . import views
from django.contrib import admin
from orders.views import delete_address,cancel_order,return_order

urlpatterns = [
  path('register/', views.register, name='signup'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('admin',admin.site.urls),
  path('forgotpassword',views.forgot_password,name='forgot_password'),
  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
  path('register/login/', views.login, name='login_email'),
  path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
  path('resetPassword/', views.reset_password, name='reset_password'),
  path('edit_profile/', views.edit_profile, name='edit_profile'),
  path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
  path('change_password/',views.change_password,name='change_password'),
  path('add_address',views.add_address,name='add_address'),
  path('delete_address/<int:id>',delete_address,name='delete_address'),
  path('my_orders/', views.my_orders, name='my_orders'),
  path('order_details/<int:order_number>', views.order_details, name='order_details'),
  path("cancel_order/<int:id>/",cancel_order,name='cancel_order'),
  path("return_order/<int:id>/",return_order,name='return_order'),
]