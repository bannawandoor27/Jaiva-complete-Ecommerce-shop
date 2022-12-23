from django.shortcuts import render
from .models import *
from newsapi import NewsApiClient
import datetime
# Create your views here.
try:
    newsapi = NewsApiClient(api_key='bb92328e8996474ab76e59971c3ff0cd')
    all_articles = newsapi.get_everything(q='farming',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2022-11-22',
                                      to='2022-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)
except:
    pass
def all_blogs(request):
    if all_articles:
        article_list = all_articles['articles'][:15]
        for article in article_list:
            time =str(article['publishedAt'][:10]) 
            article['publishedAt'] = time
    else:
        article_list = []
    # print(article_list[:1])
    recent_blogs = Blog.objects.all().order_by('modified_date')[:6]
    allblogs = Blog.objects.all()
    # print(all_articles)
    context = {
      'recent_blogs' : recent_blogs,
      'all_blogs'    : allblogs,
      'article_list' : article_list,
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