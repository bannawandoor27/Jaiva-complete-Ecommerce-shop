from django.db import models

# Create your models here.
class Blog(models.Model):
    heading = models.CharField(max_length=200,blank=False)
    modified_date = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='photos/blog', blank=False)