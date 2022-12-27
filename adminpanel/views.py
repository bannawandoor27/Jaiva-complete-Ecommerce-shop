from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
# Create your views here.
from django.contrib import messages
from datetime import datetime,date,timedelta
from accounts.models import *
from orders.models import *
import calendar
def admin_login(request):
      if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_superadmin:
                login(request, user)
                # messages.success(request,'You are logged in')
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'invalid credientail')
            return redirect('admin_login')

      return render(request, 'admin_panel/admin_login.html')

def admin_dashboard(request):
    customers_count = Account.objects.filter(is_admin=False).count()
    orders_count = Order.objects.filter(is_ordered=True).count()
    product_count = Product.objects.filter(is_available=True).count()
    total_orders = Order.objects.filter(is_ordered=True)
    total_sales = round(sum(list(map(lambda x : x.order_total,total_orders))),2)
    today = datetime.today()
    this_year = today.year
    this_month = today.month
    label_list = []
    data_list = []
    month_list = list(map(lambda x : calendar.month_name[x],range(1,this_month+1)))
    for year in range(2022,(this_year+1)):
        for month in range(1,(this_month+1)):
            month_wise_total_orders = Order.objects.filter(is_ordered=True,created_at__year = year,created_at__month=month,).order_by('created_at').count()
            month_name = calendar.month_abbr[month]
            label_update = str(year)+ str(month_name)
            label_list.append(label_update)
            data_list.append(month_wise_total_orders)
           
    print(label_list,data_list)
    context = {
        'total_customers' : customers_count,
        'total_orders'    : orders_count,
        'total_products'  : product_count,
        'total_sales'     : total_sales,
        'month_list'      : month_list,
        'line_labels'     : label_list,
        'line_data'       : data_list,
    }
    return render(request,'admin_panel/admin_dashboard.html',context)

@staff_member_required(login_url='admin_login')
def admin_logout(request):
    if 'email' in request.session:
        request.session.flush()
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('admin_login')

def admin_dashboard_monthwise(request,month):
    today = datetime.today()
    year = today.year
    day = today.day
    selected_month = month
    month = datetime.strptime(month, '%B').month
    customers_count = Account.objects.filter(is_admin=False,date_jointed__year= year,date_jointed__month=month).count()
    orders_count = Order.objects.filter(is_ordered=True,created_at__year = year,created_at__month=month,).count()
    product_count = Product.objects.filter(is_available=True,created_date__year=year,created_date__month=month).count()
    total_orders = Order.objects.filter(is_ordered=True,created_at__year = year,created_at__month=month,).order_by('created_at')
    total_sales = round(sum(list(map(lambda x : x.order_total,total_orders))),2)
    month_list = list(map(lambda x : calendar.month_name[x],range(1,today.month+1)))
    # x= total_orders[0].created_at.date().day
    order_count_per_day = []
    for day in range (1,(day+1)):
        day_order = Order.objects.filter(is_ordered=True,created_at__year = year,created_at__month=month, created_at__day=day).count()
        order_count_per_day.append(day_order)
    days = list(range(1,day+1))
    sales_per_day =[]
    for day in range (1,(day+1)):
        day_order = Order.objects.filter(is_ordered=True,created_at__year = year,created_at__month=month, created_at__day=day)
        day_sales = sum(list(map(lambda x : x.order_total,day_order)))
        sales_per_day.append(day_sales)

    context = {
        'total_customers' : customers_count,
        'total_orders'    : orders_count,
        'total_products'  : product_count,
        'total_sales'     : total_sales,
        'month_list'      : month_list,
        'selected_month'  : selected_month,
        'line_labels'     : days,
        'line_data'       : order_count_per_day,
        'bar_data'        : sales_per_day
    }
    
    return render(request,'admin_panel/admin_dashboard.html',context)
