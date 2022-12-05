from django.contrib import admin
from .models import Account,Address
# Register your models here.
admin.site.register(Account)
admin.site.register(Address)

from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display =('email','first_name','last_name','username','last_login','date_jointed','is_active')
    list_filter=()
    filter_horizontal=()
    fieldsets=()
class Address(admin.ModelAdmin):     
    list_display: tuple(('user','city','district','state','country'))
