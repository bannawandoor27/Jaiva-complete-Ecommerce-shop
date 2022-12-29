from django.shortcuts import render
from .models import *
from newsapi import NewsApiClient
from datetime import timedelta,date
from django.conf import settings
# Create your views here.
try:
    
    newsapi = NewsApiClient(api_key= settings.API_KEY)
    today = str( date.today().strftime("%Y-%m-%d"))
    ten_days_before = str((date.today()-timedelta(days=10)).isoformat())
    all_articles = newsapi.get_everything(q='farming',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param= ten_days_before,
                                      to= today,
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)
    print(1)                                  
except:
    pass
def all_blogs(request):
    try:
        if all_articles:
            article_list = all_articles['articles'][:15]
            for article in article_list:
                time =str(article['publishedAt'][:10]) 
                article['publishedAt'] = time
        else:
            article_list = []
    except:
        article_list=[]
    
    allblogs = Blog.objects.all().order_by('-modified_date')
    context = {
      'recent_blogs' : allblogs[:6],
      'all_blogs'    : allblogs,
      'article_list' : article_list,
    }
    
    return render(request,'blog/blog.html',context)

def blog_details(request,id):
    blog = Blog.objects.get(id=id)
    recent_blogs = Blog.objects.all().order_by('-modified_date')[:6]
    context= {
        'blog':blog,
        'recent_blogs': recent_blogs
    }
    return render(request,'blog/blog_details.html',context)