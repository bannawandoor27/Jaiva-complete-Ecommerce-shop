from django.urls import path,include
from . import views

urlpatterns = [
    path('login',views.admin_login,name='admin_login'),
    path('dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('/logout/', views.admin_logout, name='admin_logout'),
    
]