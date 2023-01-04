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
    path('admin_user_management',views.admin_user_management,name='admin_user_management'),
    path('<int:id>/edit_user_data/', views.edit_user_data, name='edit_user_data'),
    path('<int:id>/block_user/', views.block_user, name='block_user'),
    path('admin_categories',views.admin_categories,name='admin_categories'),
    path('<str:category_slug>/edit_category',views.admin_edit_category,name='admin_edit_category'),
    path('<str:category_slug>/delete_category',views.admin_delete_category,name='admin_delete_category'),
    path('add_category',views.admin_add_category,name='admin_add_category'),
    path('category_offers/', views.category_offers, name='category_offers'),
    path('add_category_offer/', views.add_category_offer, name='add_category_offer'),
    path('delete_category_offer/<int:id>/', views.delete_category_offer, name='delete_category_offer'),
    path('<str:category_slug>/subcategories/', views.subcategories, name='admin_subcategories'),
    path('<str:category_slug>/add_subcategory/', views.add_subcategory, name='admin_add_subcategory'),
    path('<str:slug>/edit_subcategory/', views.edit_subcategory, name='edit_subcategory'),
    path('<str:slug>/delete_subcategory/', views.delete_subcategory, name='delete_subcategory'),
]