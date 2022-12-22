from django.shortcuts import render
from .models import *
# Create your views here.

def all_blogs(request):

    recent_blogs = Blog.objects.all().order_by('modified_date')[:6]
    allblogs = Blog.objects.all()
    context = {
      'recent_blogs' : recent_blogs,
      'all_blogs'    : allblogs
    }
    return render(request,'blog/blog.html',context)

def blog_details(request,id):
    blog = Blog.objects.get(id=id)
    recent_blogs = Blog.objects.all().order_by('modified_date')[:6]
    context= {
        'blog':blog,
        'recent_blogs': recent_blogs
    }
    return render(request,'blog/blog_details.html',context)