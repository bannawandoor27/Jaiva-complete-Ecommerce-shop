from .models import Blog

def blog_data(request):
    blog_data = Blog.objects.all().order_by('-modified_date')[:3]
    return dict(blog_data=blog_data)