from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import Address
from django.contrib import messages, auth
import datetime
from carts.models import CartItem
from .models import Order, Address, Payment, OrderProduct, Coupon, UserCoupon
from jaivashop.models import Product
from django.http import JsonResponse
from django.conf import settings
import razorpay
# Create your views here.

@login_required(login_url='login')
def delete_address(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('checkout')

def coupon(request):
  if request.method == 'POST':
    coupon_code = request.POST['coupon']
    grand_total = request.POST['grand_total']
    coupon_discount = 0
    try:
      instance = UserCoupon.objects.get(user = request.user ,coupon__code = coupon_code)

      if float(grand_total) >= float(instance.coupon.min_value):
        coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
        grand_total = float(grand_total) - coupon_discount
        grand_total = format(grand_total, '.2f')
        coupon_discount = format(coupon_discount, '.2f')
        msg = 'Coupon Applied successfully'
        instance.used = True
        instance.save()
      else:
          msg='This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!'
    except:
            msg = 'Coupon is not valid'
    response = {
               'grand_total': grand_total,
               'msg':msg,
               'coupon_discount':coupon_discount,
               'coupon_code':coupon_code,
                }

  return JsonResponse(response)



