from django.shortcuts import render, redirect
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages, auth
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .otptest import *

# Create your views here.


def register(request):
  if 'email' in request.session:
    return redirect('home')
  
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password']
      
      user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
      user.save()
      request.session['phone_number'] = phone_number
      
    #   send_otp(phone_number)
      return redirect('login')
      # messages.success(request, 'Registration Successful')  # registration without otp
      # return redirect('login')
  else:    
    form = RegistrationForm()
  context = {
    'form': form
  }
  
  return render (request, 'Customers/signup.html', context)

@never_cache
def login(request):
  if 'email' in request.session:
    return redirect('home')
  
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
        
    user = auth.authenticate(email=email, password=password)

    if user is not None:
           
      auth.login(request, user)      # login without otp
      request.session['email'] = email
    #   messages.success(request, 'You are now logged in.')
      return redirect('home')    
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
    
  return render (request, 'Customers/login.html')

def otpLogin(request):
  if request.user.is_authenticated:
      return redirect('home')
  
  if request.method == 'POST':
    phone_number = request.POST.get('phone_number')
    request.session['phone_number'] = phone_number
    try:
      user = Account.objects.get(phone_number=phone_number)
    except:
      messages.error(request, 'Mobile number not registered!!!')
      return redirect('otpLogin')
    
    send_otp(phone_number)
    return redirect('otpVerification')
  
  return render(request, 'Customers/otpLogin.html')

def otpVerification(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  phone_number = request.session['phone_number']
  
  if request.method == 'POST':
    # request.session.pop('phone_number', None)
    # request.session.modified = True
    user = Account.objects.get(phone_number=phone_number)
    try:
      check_otp = request.POST.get('otp')
      if not check_otp:
        raise e
    except Exception as e:
      messages.error(request, 'Please type in your OTP!!!')
      return redirect('otpVerification')
    
    check = verify_otp(phone_number, check_otp)
    
    if check:
      if user.is_active:
        auth.login(request, user)
        request.session['email'] = user.email
        return redirect('home')
      
      else:
        user.is_active = True
        user.save()
        messages.success(request, 'Account Verified.')
        return redirect('login')
    
    else:
      messages.error(request, 'Invalid OTP!!!')
      return redirect('otpVerification')
    
  context = {
    'phone_number':phone_number
  }
  return render(request, 'Customers/otpVerification.html', context)

@login_required(login_url = 'login')
def logout(request):
  if 'email' in request.session:
    request.session.flush()
  auth.logout(request)
  messages.success(request, "You are logged out.")
  return redirect('login')