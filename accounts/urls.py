from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
  path('/register/', views.register, name='signup'),
  path('/login/', views.login, name='login'),
  path('/otpLogin/', views.otpLogin, name='otpLogin'),
  path('/otpVerification', views.otpVerification, name='otpVerification'),
  path('/logout/', views.logout, name='logout'),
  path('/profile',views.profile,name='profile'),
  path('/admin',admin.site.urls),
]