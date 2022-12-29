from django.urls import path,include
from . import views

urlpatterns = [
    path('login',views.admin_login,name='admin_login'),
    path('dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/<slug:month>', views.admin_dashboard_monthwise,name='admin_dashboard_monthwise'),
    path('admin_messages',views.admin_messages,name='admin_messages'),
    path('delete_message/<int:id>',views.delete_message,name='delete_message'),
    path('reply_message',views.reply_message,name='reply_message'),
    path('admin_blog',views.admin_blog,name='admin_blog'),
    path('add_blog',views.add_blog,name='add_blog'),
    path('delete_blog/<int:id>',views.delete_blog,name='delete_blog'),
    path('edit_blog/<int:id>',views.edit_blog,name='edit_blog'),
    path('edit_blog_single/<int:id>',views.edit_blog_single,name='edit_blog_single'),
    
]