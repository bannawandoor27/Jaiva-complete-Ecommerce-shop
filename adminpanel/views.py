from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from category.models import Category, Sub_Category
from jaivashop.models import ContactMessage
# Create your views here.
from django.contrib import messages
from datetime import datetime,date,timedelta
from accounts.models import *
from orders.models import *
import calendar
from django.db.models import Q
from django.db.models import Sum,FloatField
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import never_cache
from .forms import LoginForm, ProductForm, CategoryForm, SubCategoryForm, UserForm, CouponForm,BlogForm
from django.core.mail import EmailMessage
from blog.models import Blog
from django.core.paginator import Paginator
from django.utils import timezone
@never_cache
def admin_login(request):
  if 'email' in request.session:
    return redirect('admin_dashboard')
    
  if request.method == 'POST':
    # form = LoginForm(request.POST)
    email = request.POST['email']
    password = request.POST['password']
    
    user = authenticate(email=email, password=password)
    
    if user is not None:
      if user.is_superadmin:
        request.session['email'] = email
        
        login(request, user)
        return redirect('admin_dashboard')
        
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

@staff_member_required(login_url = 'admin_login')
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
@staff_member_required(login_url = 'admin_login')
def admin_dashboard_monthwise(request,month):
    total_orders = Order.objects.filter(is_ordered=True).order_by('created_at')
    first_order_date = total_orders[0].created_at.date()
    taken_month = month
    selected_month = taken_month[:3]
    selected_year = taken_month[4:9]
    today = datetime.today()
    selected_month_num = datetime.strptime(selected_month, '%b').month
    month_range  =calendar.monthrange(int(selected_year),int(selected_month_num))[1]
    
    day = today.day if selected_year==today.year else month_range
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
@staff_member_required(login_url = 'admin_login')
def admin_messages(request):
    messages_recieved  = ContactMessage.objects.all().order_by('-sent_time')
    context = {
        'messages_recieved' : messages_recieved,
    }
    return render(request,'admin_panel/admin_messages.html',context)
@staff_member_required(login_url = 'admin_login')
def delete_message(request,id):
    message = ContactMessage.objects.get(id=id)
    message.delete()
    messages.error(request,'message deleted successfully!')
    return redirect('admin_messages')
@staff_member_required(login_url = 'admin_login')
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
@staff_member_required(login_url = 'admin_login')
def admin_blog(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
      'blogs':page_obj
    }
    return render(request,'admin_panel/blog_management/admin_blog.html',context)
@staff_member_required(login_url = 'admin_login')
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
@staff_member_required(login_url = 'admin_login')
def delete_blog(request,id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    messages.success(request,'Post deleted successfully')
    return redirect('admin_blog')
@staff_member_required(login_url = 'admin_login')
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
@staff_member_required(login_url = 'admin_login')
def edit_blog_single(request,id):
    post = Blog.objects.get(id=id)
    context = dict(
    post_heading = post.heading,
    post_category = post.category,
    post_description = post.description
    )
    return JsonResponse(context)


# Admin User Management
@staff_member_required(login_url = 'admin_login')
def admin_user_management(request):
  if request.method == 'POST':
    search_key = request.POST.get('search')
    users = Account.objects.filter(Q(first_name__icontains=search_key) | Q(last_name__icontains=search_key) | Q(email__icontains=search_key),is_superadmin=False)
    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
  else:
    users = Account.objects.all().filter(is_superadmin=False).order_by('-id')
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
  context = {
    'users': page_obj
  }
  return render(request,'admin_panel/user_management/admin_user_management.html',context)

@staff_member_required(login_url = 'admin_login')
def edit_user_data(request, id):
  user = Account.objects.get(id=id)
  
  if request.method == 'POST':
    form = UserForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
      form.save()
      messages.success(request, 'User Account edited successfully.')
      return redirect('admin_user_management')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('edit_user_data', id)
    
  else:
    form = UserForm(instance=user)
  
  context = {
    'form':form,
    'id':id,
  }
    
  return render(request, 'admin_panel/user_management/edit_user_data.html', context)

@staff_member_required(login_url = 'admin_login')
def block_user(request, id):
    users = Account.objects.get(id=id)
    if users.is_active:
        users.is_active = False
        users.save()

    else:
         users.is_active = True
         users.save()

    return redirect('admin_user_management')

# Admin Category Management
@staff_member_required(login_url = 'admin_login')
def admin_categories(request):
  categories = Category.objects.all().order_by('id')
  
  paginator = Paginator(categories, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'categories':page_obj
  }
  return render(request, 'admin_panel/category_management/admin_categories.html', context)

@staff_member_required(login_url = 'admin_login')
def admin_add_category(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Category added successfully.')
      return redirect('admin_categories')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('admin_add_category')
  else:
    form = CategoryForm()
    context = {
      'form':form,
    }
    return render(request, 'admin_panel/category_management/admin_add_category.html', context)
  
@staff_member_required(login_url = 'admin_login')
def admin_edit_category(request, category_slug):
  category = Category.objects.get(slug=category_slug)
  
  if request.method == 'POST':
    form = CategoryForm(request.POST, request.FILES, instance=category)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Category edited successfully.')
      return redirect('admin_categories')
    else:
      messages.error(request, 'Invalid input')
      return redirect('admin_edit_category', category_slug)
      
  form =   CategoryForm(instance=category)
  context = {
    'form':form,
    'category':category,
  }
  return render(request, 'admin_panel/category_management/admin_edit_category.html', context)
  
@staff_member_required(login_url = 'admin_login')  
def admin_delete_category(request, category_slug):
  category = Category.objects.get(slug=category_slug)
  category.delete()
  messages.success(request, 'Category deleted successfully.')
  return redirect('admin_categories')

#  Admin Category Offers
@staff_member_required(login_url = 'admin_login')  
def category_offers(request):
  categories = Category.objects.all().order_by('-category_offer')
  
  paginator = Paginator(categories, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'categories':page_obj,
  }
  return render(request, 'admin_panel/category_management/admin_category_offers.html', context)

@staff_member_required(login_url= 'admin_login')
def add_category_offer(request):
  if request.method == 'POST' :
    category_name = request.POST.get('category_name')
    category_offer = request.POST.get('category_offer')
    category = Category.objects.get(category_name = category_name)
    category.category_offer =  category_offer
    category.save()
    messages.success(request,'Category offer added successfully')
    return redirect('category_offers')
      
@staff_member_required(login_url= 'admin_login')
def delete_category_offer(request, id):
  category = Category.objects.get(id = id)
  category.category_offer =  0
  category.save()
  messages.success(request,'Category offer deleted successfully')
  return redirect('category_offers')


# Subcategory management

@staff_member_required(login_url = 'admin_login')
def subcategories(request, category_slug):
  sub_categories = Sub_Category.objects.all().filter(category__slug=category_slug)
  context = {
    'sub_categories':sub_categories,
    'category_slug':category_slug,
  }
  return render(request, 'admin_panel/category_management/admin_subcategories.html', context)

@staff_member_required(login_url = 'admin_login')
def add_subcategory(request, category_slug):
  category = Category.objects.get(slug=category_slug)
  if request.method == 'POST':
    form = SubCategoryForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Subcategory added successfully.')
      return redirect('admin_subcategories', category_slug)
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('admin_add_subcategory', category_slug)
  else:
    form = SubCategoryForm()
    context = {
      'form':form,
      'category':category
    }
    return render(request, 'admin_panel/category_management/add_subcategory.html', context)
  
@staff_member_required(login_url = 'admin_login')
def edit_subcategory(request, slug):
  sub_category = Sub_Category.objects.get(slug=slug)
  cat_slug = sub_category.category.slug
  
  if request.method == 'POST':
    form = SubCategoryForm(request.POST, request.FILES, instance=sub_category)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Subcategory edited successfully.')
      return redirect('admin_subcategories', cat_slug)
    else:
      messages.error(request, 'Invalid input')
      return redirect('edit_subcategory')
      
  form =   SubCategoryForm(instance=sub_category)
  context = {
    'form':form,
    'sub_category':sub_category,
  }
  return render(request, 'admin_panel/category_management/admin_edit_subcategory.html', context)

@staff_member_required(login_url = 'admin_login')  
def delete_subcategory(request, slug):
  sub_category = Sub_Category.objects.get(slug=slug)
  category_slug = sub_category.category.slug
  sub_category.delete()
  messages.success(request, 'Subcategory deleted successfully.')
  return redirect('admin_subcategories', category_slug)
 

 
# Product management
  
@staff_member_required(login_url = 'admin_login')
def admin_products(request):
  if request.method == 'POST':
    search_key = request.POST.get('search')
    products = Product.objects.filter(Q(product_name__icontains=search_key))
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
  else:
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
  
  context = {
    'products': page_obj
  }
  return render(request, 'admin_panel/product_management/admin_products.html', context)

@staff_member_required(login_url = 'admin_login')
def admin_add_product(request):
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Product added successfully.')
      return redirect('admin_products')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('admin_add_product')
  else:
    form = ProductForm()
    context = {
      'form':form,
    }
    return render(request, 'admin_panel/product_management/admin_add_product.html', context)

@staff_member_required(login_url = 'admin_login')
def admin_edit_product(request, id):
  product = Product.objects.get(id=id)
  
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES, instance=product)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'product data edited successfully.')
      return redirect('admin_products')
    else:
      messages.error(request, 'Invalid parameters')
      
  form =   ProductForm(instance=product)
  context = {
    'form':form,
    'product':product,
  }
  return render(request, 'admin_panel/product_management/admin_edit_product.html', context)

@staff_member_required(login_url = 'admin_login')  
def admin_delete_product(request, id):
  product = Product.objects.get(id=id)
  product.delete()
  return redirect('admin_products')

@staff_member_required(login_url = 'admin_login')  
def admin_product_offers(request):
  products = Product.objects.all().order_by('-product_offer')
  
  paginator = Paginator(products, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'products':page_obj,
  }
  return render(request, 'admin_panel/product_management/admin_product_offers.html', context)

@staff_member_required(login_url= 'admin_login')
def add_product_offer(request):
  if request.method == 'POST' :
    product_name = request.POST.get('product_name')
    product_offer = request.POST.get('product_offer')
    product = Product.objects.get(product_name = product_name)
    product.product_offer =  product_offer
    product.save()
    messages.success(request,'Product offer added successfully')
    return redirect('admin_product_offers')
  
@staff_member_required(login_url= 'admin_login')
def delete_product_offer(request, id):
  product = Product.objects.get(id=id)
  product.product_offer = 0
  product.save()
  messages.success(request, 'Product offer deleted successfully')
  return redirect('admin_product_offers')

@staff_member_required(login_url = 'admin_login')
def admin_orders(request):
  orders = Order.objects.filter(is_ordered=True).order_by('id')
  paginator = Paginator(orders, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  
  
  context = {
    'orders':page_obj,
  }
  return render(request, 'admin_panel/order_management/admin_orders.html', context)

@staff_member_required(login_url = 'admin_login')
def admin_change_order(request, id):
  if request.method == 'POST':
    order = get_object_or_404(Order, id=id)
    status = request.POST.get('status')
    order.status = status 
    order.save()
    if status  == "Delivered":
      try:
          payment = Payment.objects.get(payment_id = order.order_number, status = False)
          if payment.payment_method == 'Cash On Delivery':
              payment.status = True
              payment.save()
      except:
          pass
  return redirect('admin_orders')



@staff_member_required(login_url = 'admin_login')
def admin_coupons(request):
  coupons = Coupon.objects.all()
  context = {
    'coupons':coupons,
  }
  return render(request, 'admin_panel/coupon_management/admin_coupons.html', context)

@staff_member_required(login_url = 'admin_login')
def admin_add_coupon(request):
  if request.method == 'POST':
    form = CouponForm(request.POST , request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request,'Coupon Added successfully')
      return redirect('admin_coupons')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('admin_add_coupon')
  form = CouponForm()
  context = {
    'form':form,
  }
  return render(request, 'admin_panel/coupon_management/admin_add_coupon.html', context)

@staff_member_required(login_url = 'admin_login')
def admin_edit_coupon(request, id):
  coupon = Coupon.objects.get(id = id)
  if request.method == 'POST':
    form = CouponForm(request.POST , request.FILES, instance=coupon)
    if form.is_valid():
      form.save()
      messages.success(request,'Coupon updated successfully')
      return redirect('admin_coupons')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('admin_edit_coupon', coupon.id)
  form = CouponForm(instance=coupon)
  context = {
    'coupon':coupon,
    'form':form,
  }
  return render(request, 'admin_panel/coupon_management/admin_edit_coupon.html', context)

@staff_member_required(login_url= 'admin_login')
def admin_delete_coupon(request, id):
  coupon = Coupon.objects.get(id = id)
  coupon.delete()
  messages.success(request,'Coupon deleted successfully')
  return redirect('admin_coupons')

@staff_member_required(login_url= 'admin_login')
def admin_sales_data(request):
    total_orders = Order.objects.filter(is_ordered=True).order_by('created_at')
    first_order_date = total_orders[0].created_at.date()
    today = timezone.now()
    day = today.day
    month = today.month
    year = today.year
    month_list = []
    for i in range(1,13):month_list.append(calendar.month_name[i]) 
    year_list = []
    for i in range(first_order_date.year,year+1):year_list.append(i)
    this_date=str(today.date())
    start_date=this_date
    end_date=this_date
    filter= False
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        temp = start_date
        end_date = request.POST.get('end_date')
        # converting from naive to timezone aware
        val = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
        start_date = timezone.make_aware(datetime.strptime(temp, '%Y-%m-%d'))
        end_date = val+timedelta(days=1)
        filter=True
        orders = Order.objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date)).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
    else:
        orders = Order.objects.filter(created_at__year = year,created_at__month=month).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')

    context = {
        'month_list':month_list,
        'orders':orders,
        'this_date':this_date,
        'year_list':year_list,
        'start_date':start_date,
        'end_date':end_date,
        'filter':filter
        
    }
    return render(request, 'admin_panel/admin_sales_data.html', context)

