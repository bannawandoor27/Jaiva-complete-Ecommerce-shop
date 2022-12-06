from django.contrib import admin

# Register your models here.

from .models import Blog

class BlogAdmin(admin.ModelAdmin):
  list_display = ('heading','modified_date','description')

admin.site.register(Blog,BlogAdmin)