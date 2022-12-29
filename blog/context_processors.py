from .models import Blog

def blog_data(request):
    blog_data = Blog.objects.all().order_by('-modified_date')
    return dict(blog_data=blog_data[:3],all_new_blogs=blog_data)