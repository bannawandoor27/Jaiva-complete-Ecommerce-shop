from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
  path('/register/', views.register, name='signup'),
  path('/login/', views.login, name='login'),
  path('/logout/', views.logout, name='logout'),
  path('/profile',views.profile,name='profile'),
  path('/admin',admin.site.urls),
  path('/forgotpassword',views.forgot_password,name='forgot_password'),
  path('activate/<uidb64>/<token>/', views.activate, name='activate'),
  path('/register/login/', views.login, name='login_email'),
  path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
  path('resetPassword/', views.reset_password, name='reset_password'),
]