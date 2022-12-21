from django.db import models

# Create your models here.
class Blog(models.Model):

    heading = models.CharField(max_length=200,blank=False)
    modified_date = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=50,default = 'general')
    description = models.TextField(max_length=10000, blank=True)
    image = models.ImageField(upload_to='photos/blog', blank=False)