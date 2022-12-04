from django.shortcuts import render, redirect
from .models import Account, Address
from .forms import RegistrationForm, UserAddressForm, UserForm
from django.contrib import messages, auth
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .otptest import *
from django.shortcuts import render, get_object_or_404
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
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
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
            user.save()
            # Create Address Automatically
            # address=Address()
            # address.pk= user.id
            # address.save()
            request.session['phone_number'] = phone_number
            
            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('Customers/account_verify_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            return redirect('login/?command=verification&email='+email)
        else:
            messages.error(request, 'please fill the form correctly!')
    else:
        form = RegistrationForm()
        
    context = {
        'form': form
    }

    return render(request, 'Customers/signup.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('signup')





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

    return render(request, 'Customers/login.html')




@login_required(login_url='login')
def logout(request):
    if 'email' in request.session:
        request.session.flush()
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('login')

def profile(request):
    useraddress = get_object_or_404(Address, user = request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        address_form = UserAddressForm(request.POST, instance=useraddress)
        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        # else:
        #     context={'error':user_form.errors,

        #             'error2':address_form.errors
            
        #     }
        #     return render(request, 'profile.html', context)
    else:
         user_form = UserForm(instance=request.user)
         address_form = UserAddressForm(instance=useraddress)
         context = {
                'user_form': user_form,
                'address_form': address_form
            }
        #  full_name = str(user.first_name) + str(user.last_name)   
    return render(request, 'profile.html', context)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('Customers/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'Customers/forgot_password.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    else:
        return render(request, 'Customers/reset_password.html')









































# def otpLogin(request):
#     if request.user.is_authenticated:
#         return redirect('home')

#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#         request.session['phone_number'] = phone_number
#         try:
#             user = Account.objects.get(phone_number=phone_number)
#         except:
#             messages.error(request, 'Mobile number not registered!!!')
#             return redirect('otpLogin')

#         send_otp(phone_number)
#         return redirect('otpVerification')

#     return render(request, 'Customers/otpLogin.html')

# def otp_forgot_password(request):
#     phone_number = request.session['phone_number']
#     if request.method == 'POST':
#         user = Account.objects.get(phone_number=phone_number)
#         try:
#             check_otp = request.POST.get('otp')
#             if not check_otp:
#                 raise e
#         except Exception as e:
#             messages.error(request, 'Please type in your OTP!!!')
#             return redirect('otpforgotpassword')

#         check = verify_otp(phone_number, check_otp)
#         if check:
#             messages.success(request,"OTP verified successfully")
#             return redirect('resetpassword')

# def reset_password(request):
#     if request.method == 'POST':
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']
#         if len(password)<8 or len(confirm_password)<8:
#             messages.error(request,'password must contain atleast 8 characters!')
#             return redirect('resetpassword')
#         elif password!=confirm_password:
#             messages.error(request,'Passwords doesnoty match!')
#             return redirect('resetpassword')
#         else:
#             uid = request.session.get('uid')
#             user = Account.objects.get(pk=uid)
#             user.set_password(password)
#             user.save()
#             messages.success(request,'Password reset successful')
#     return render(request,'Customers/reset_password.html')


# def otpVerification(request):
    # if request.user.is_authenticated:
    #     return redirect('home')

    # phone_number = request.session['phone_number']

    # if request.method == 'POST':
    #     # request.session.pop('phone_number', None)
    #     # request.session.modified = True
    #     user = Account.objects.get(phone_number=phone_number)
    #     try:
    #         check_otp = request.POST.get('otp')
    #         if not check_otp:
    #             raise e
    #     except Exception as e:
    #         messages.error(request, 'Please type in your OTP!!!')
    #         return redirect('otpVerification')

    #     check = verify_otp(phone_number, check_otp)

    #     if check:
    #         if user.is_active:
    #             auth.login(request, user)
    #             request.session['email'] = user.email
    #             return redirect('home')

    #         else:
    #             user.is_active = True
    #             user.save()
    #             messages.success(request, 'Account Verified.')
    #             return redirect('login')

    #     else:
    #         messages.error(request, 'Invalid OTP!!!')
    #         return redirect('otpVerification')

    # context = {
    #     'phone_number': phone_number
    # }
    # return render(request, 'Customers/otpVerification.html', context)