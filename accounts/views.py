from django.shortcuts import render, redirect
import requests

from carts.models import Cart, CartItem
from carts.views import _cart_id
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
from django.contrib.auth import update_session_auth_hash
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
            address = Address.objects.create(user=user)
            address.save()
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
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
        
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []
                    for item in cart_item:
                        variations = item.variations.all()
                        product_variation.append(list(variations))
                    cart_item = CartItem.objects.filter(user=user)

                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for product in product_variation:
                        if product in ex_var_list:
                            index = ex_var_list.index(product)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)    
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass



            auth.login(request, user)      # login without otp
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
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

def edit_profile(request):
    useraddress = Address.objects.all().filter(user=request.user).first()
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        address_form = UserAddressForm(request.POST, instance=useraddress)
        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('edit_profile')
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
    return render(request, 'Customers/edit_profile.html', context)

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





@login_required(login_url='userLogin')
def add_address(request):
    if request.method == 'POST':
        form = UserAddressForm(request.POST,request.FILES,)
        if form.is_valid():
            print('form is valid')
            address = Address()
            address.user = request.user
            address.address_line_1 =  form.cleaned_data['address_line_1']
            address.address_line_2  = form.cleaned_data['address_line_2']
            address.district =  form.cleaned_data['district']
            address.state =  form.cleaned_data['state']
            address.city =  form.cleaned_data['city']
            address.country = form.cleaned_data['country']
            address.pin_code =  form.cleaned_data['pin_code']
            address.save()
            messages.success(request,'Address added Successfully')
            return redirect('edit_profile')
        else:
            messages.success(request,'Form is Not valid')
            return redirect('add_address')
    else:
        form = UserAddressForm()
        context={
            'form':form
        }    
    return render(request,'Customers/add_address.html',context)

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

@login_required
def user_dashboard(request):
    return render(request,'Customers/dashboard.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(phone_number__exact=request.user.phone_number)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                # auth.logout(request)
                messages.success(request, 'Password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'Customers/change_password.html')




































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