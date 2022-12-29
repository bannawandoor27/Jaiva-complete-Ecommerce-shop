from django.urls import path,include
from . import views

urlpatterns = [
    path('login',views.admin_login,name='admin_login'),
    path('dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/<slug:month>', views.admin_dashboard_monthwise,name='admin_dashboard_monthwise'),
    path('admin_messages',views.admin_messages,name='admin_messages'),
    path('delete_message/<int:id>',views.delete_message,name='delete_message'),
    path('reply_message',views.reply_message,name='reply_message')
    
]