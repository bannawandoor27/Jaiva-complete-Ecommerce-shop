from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from jaivashop.models import ContactMessage
# Create your views here.
from django.contrib import messages
from datetime import datetime,date,timedelta
from accounts.models import *
from orders.models import *
import calendar
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from .forms import LoginForm, ProductForm, CategoryForm, SubCategoryForm, UserForm, CouponForm, VariationForm,BlogForm
from django.core.mail import EmailMessage
from blog.models import Blog
@never_cache
def admin_login(request):
  if 'email' in request.session:
    return redirect('dashboard')
    
  if request.method == 'POST':
    # form = LoginForm(request.POST)
    email = request.POST['email']
    password = request.POST['password']
    
    user = authenticate(email=email, password=password)
    
    if user is not None:
      if user.is_superadmin:
        request.session['email'] = email
        
        login(request, user)
        return redirect('dashboard')
        
      else:
        messages.error(request, 'You are not autherized to access admin panel')
        return redirect('admin_login')
    else:
      messages.error(request, 'Invalid login credentials')
      return redirect('admin_login')
    
  form = LoginForm
  return render(request, 'admin_panel/admin_login.html', {'form':form})
  
@staff_member_required(login_url='admin_login')
def admin_logout(request):
    if 'email' in request.session:
        request.session.flush()
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('admin_login')

def admin_dashboard(request):
    customers_count = Account.objects.filter(is_admin=False).count()
    orders_count = Order.objects.filter(is_ordered=True).count()
    product_count = Product.objects.filter(is_available=True).count()
    total_orders = Order.objects.filter(is_ordered=True).order_by('created_at')
    first_order_date = total_orders[0].created_at.date()
    total_sales = round(sum(list(map(lambda x : x.order_total,total_orders))),2)
    today = datetime.today()
    this_year = today.year
    this_month = today.month
    label_list = []
    line_data_list = []
    bar_data_list =  []
    month_list=[]
    for year in range(first_order_date.year,this_year+1) :
        month = this_month if year==this_year else 12
        month_list= month_list+(list(map(lambda x : calendar.month_abbr[x]+'-'+str(year),range(1,month+1))))[::-1]
    for year in range(2022,(this_year+1)):
        this_month = this_month if year==this_year else 12
        for month in range(1,(this_month+1)):
            month_wise_total_orders = Order.objects.filter(is_ordered=True,created_at__year = year,created_at__month=month,).order_by('created_at').count()
            month_name = calendar.month_abbr[month]
            label_update = str(month_name)+ ' ' + str(year)
            label_list.append(label_update)
            line_data_list.append(month_wise_total_orders)
    for year in range(2022,(this_year+1)):
        for month in range(1,(this_month+1)):
            monthwise_orders = Order.objects.filter(is_ordered=True,created_at__year = year,created_at__month=month,)
            monthwise_sales  = round(sum(list(map(lambda x : x.order_total,monthwise_orders))),2)
            bar_data_list.append(monthwise_sales)



     
    context = {
        'total_customers' : customers_count,
        'total_orders'    : orders_count,
        'total_products'  : product_count,
        'total_sales'     : total_sales,
        'month_list'      : month_list,
        'line_labels'     : label_list,
        'line_data'       : line_data_list,
        'bar_data'        : bar_data_list
    }
    return render(request,'admin_panel/admin_dashboard.html',context)

def admin_dashboard_monthwise(request,month):
    total_orders = Order.objects.filter(is_ordered=True).order_by('created_at')
    first_order_date = total_orders[0].created_at.date()
    taken_month = month
    selected_month = taken_month[:3]
    selected_year = taken_month[4:9]
    today = datetime.today()
    
    day = today.day if selected_year==today.year else 31
    month = datetime.strptime(selected_month, '%b').month
    customers_count = Account.objects.filter(is_admin=False,date_jointed__year= selected_year,date_jointed__month=month).count()
    orders_count = Order.objects.filter(is_ordered=True,created_at__year = selected_year,created_at__month=month,).count()
    product_count = Product.objects.filter(is_available=True,created_date__year=selected_year,created_date__month=month).count()
    total_orders = Order.objects.filter(is_ordered=True,created_at__year = selected_year,created_at__month=month,).order_by('created_at')
    
    total_sales = round(sum(list(map(lambda x : x.order_total,total_orders))),2)
    month_list=[]
    for year in range(first_order_date.year,today.year+1) :
        month = today.month if year==today.year else 12
        month_list= month_list+(list(map(lambda x : calendar.month_abbr[x]+'-'+str(year),range(1,month+1))))[::-1]
    # x= total_orders[0].created_at.date().day
    order_count_per_day = []
    selected_month_num = datetime.strptime(selected_month, '%b').month
    for day in range (1,(day+1)):
        day_order = Order.objects.filter(is_ordered=True,created_at__year = selected_year,created_at__month=selected_month_num, created_at__day=day).count()
        order_count_per_day.append(day_order)
    days = list(range(1,day+1))
    sales_per_day =[]
    for day in range (1,(day+1)):
        day_order = Order.objects.filter(is_ordered=True,created_at__year = selected_year,created_at__month=selected_month_num, created_at__day=day)
        day_sales = sum(list(map(lambda x : x.order_total,day_order)))
        sales_per_day.append(day_sales)

    context = {
        'total_customers' : customers_count,
        'total_orders'    : orders_count,
        'total_products'  : product_count,
        'total_sales'     : total_sales,
        'month_list'      : month_list,
        'selected_month'  : taken_month,
        'line_labels'     : days,
        'line_data'       : order_count_per_day,
        'bar_data'        : sales_per_day,
    }
    
    return render(request,'admin_panel/admin_dashboard.html',context)

def admin_messages(request):
    messages_recieved  = ContactMessage.objects.all().order_by('-sent_time')
    context = {
        'messages_recieved' : messages_recieved,
    }
    return render(request,'admin_panel/admin_messages.html',context)

def delete_message(request,id):
    message = ContactMessage.objects.get(id=id)
    message.delete()
    messages.error(request,'message deleted successfully!')
    return redirect('admin_messages')

def reply_message(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            message = request.POST['message']
            mail_subject = ''' Reply from Jaiva Ecommerce shop'''
            send_mail = EmailMessage(mail_subject,message,to=[email])
            send_mail.send()
            messages.success(request,'Message sent successfully')
        else:
            messages.error(request,'please fill the form correctly')
    except:
        messages.error(request,'Server down! please ensure you are connected to internet')
    return redirect('admin_messages')

def admin_blog(request):
    return render(request,'admin_panel/admin_blog.html')

def add_blog(request):
    if request.method == 'POST':
        heading = request.POST['heading']
        category = request.POST['category']
        image = request.FILES.get('image')
        description = request.POST['description']
        new_blog = Blog.objects.create(heading=heading,category=category,image=image,description=description)
        new_blog.save()
        messages.success(request,'Blog posted successfully!')
        return redirect('admin_blog')
    else:
        return redirect('admin_blog')

def delete_blog(request,id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    messages.success(request,'Post deleted successfully')
    return redirect('admin_blog')

def edit_blog(request,id):
    post = Blog.objects.get(id=id)
    if request.method == 'POST':
        post.heading = request.POST.get('heading')
        post.category = request.POST.get('category')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.description = request.POST.get('description')
        post.save()
        messages.success(request,'Post edited successfully!')
        return redirect('admin_blog')
    else:
        messages.error(request,'Some error occured!')
        return redirect('admin_blog')

def edit_blog_single(request,id):
    post = Blog.objects.get(id=id)
    context = dict(
    post_heading = post.heading,
    post_category = post.category,
    post_description = post.description
    )
    return JsonResponse(context)
