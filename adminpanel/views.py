from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
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
    total_sales = sum(list(map(lambda x : x.order_total,total_orders)))
    today = datetime.today()
    this_month = today.month
    month_list = list(map(lambda x : calendar.month_name[x],range(1,this_month+1)))
    



    context = {
        'total_customers' : customers_count,
        'total_orders'    : orders_count,
        'total_products'  : product_count,
        'total_sales'     : total_sales,
        'month_list'      : month_list
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
    selected_month = month
    month = datetime.strptime(month, '%B').month
    customers_count = Account.objects.filter(is_admin=False,date_jointed__year= year,date_jointed__month=month).count()
    orders_count = Order.objects.filter(is_ordered=True,created_at__year = year,created_at__month=month,).count()
    product_count = Product.objects.filter(is_available=True,created_date__year=year,created_date__month=month).count()
    total_orders = Order.objects.filter(is_ordered=True,created_at__year = year,created_at__month=month,)
    total_sales = sum(list(map(lambda x : x.order_total,total_orders)))
    month_list = list(map(lambda x : calendar.month_name[x],range(1,today.month+1)))
    context = {
        'total_customers' : customers_count,
        'total_orders'    : orders_count,
        'total_products'  : product_count,
        'total_sales'     : total_sales,
        'month_list'      : month_list,
        'selected_month'  : selected_month
    }
    
    return render(request,'admin_panel/admin_dashboard.html',context)