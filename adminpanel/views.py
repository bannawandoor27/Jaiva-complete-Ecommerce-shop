from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib import messages

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
    return render(request,'admin_panel/admin_dashboard.html')

@login_required(login_url='admin_login')
def admin_logout(request):
    if 'email' in request.session:
        request.session.flush()
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect('admin_login')
