from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')

def shop(request):
    return render(request,'shop')