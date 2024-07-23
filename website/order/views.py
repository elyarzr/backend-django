from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from cart.models import *
from django.contrib.auth.decorators import login_required
from .forms import CouponForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from suds import Client
from django.http import HttpResponse


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    form = CouponForm()
    context = {'order': order, 'form': form}
    return render(request, 'order/order.html', context)


@login_required(login_url='accounts:login')
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Order.objects.create(user_id=request.user.id, email=data['email'],
                                         f_name=data['f_name'], l_name=data['l_name'], address=data['address'])
            cart = Cart.objects.filter(user_id=request.user.id)
            for c in cart:
                ItemOrder.objects.create(order_id=order.id, user_id=request.user.id, product_id=c.product_id,
                                         variant_id=c.variant_id, quantity=c.quantity)

            messages.success(request, "کاربر محترم سفارش شما با موفقیت ثبت شد", 'success')
            return redirect('order:order_detail', order.id)


@require_POST
def coupon_order(request, order_id):
    form = CouponForm(request.POST)
    time = timezone.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, start__lte=time, end__gte=time, active=True)

        except:
            messages.error(request, 'کد شما اشتباه است', 'danger')
            return redirect('order:order_detail', order_id)

        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
    return redirect('order:order_detail', order_id)



MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8080/order:verify/'


def send_request(request, price,order_id):
    global amount
    amount = price
    result = client.service.PaymentRequest(MERCHANT, amount, description, request.user.email, phone, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()
        cart = ItemOrder.objects.filter(order_id=order_id)
        for c in cart:
            if c.product.status == 'None':
                product = Product.objects.get(id=c.product.id)
                product.amount -= c.quantity
                product.save()
            else:
                variant = Variants.objects.get(id=c.variant.id)
                variant.amount -= c.quantity
                variant.save()

        return HttpResponse('Error code: ' + str(result.Status))


def verify(request):
    if request.GET.get('status') == 'ok':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'],amount)
        if result.status == 100:
            return HttpResponse('Transaction success ' )
        elif result.status == 101:
            return HttpResponse('Transaction submitted :' +str(result.status))
        else:
            return HttpResponse('Transaction faild. \nstatus:' +str(result.status))
    else:
        return HttpResponse('Transaction faild or canceled by user')


















