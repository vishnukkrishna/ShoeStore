from django.shortcuts import render, HttpResponse
from userhome.models import userAddress
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
import razorpay
from django.conf import settings
from .models import Payment,Order,OrderItem
from django.utils import timezone
# Create your views here.



@login_required(login_url= 'userlogin')
def checkOut(request):

    current_user = request.user

    addresses = userAddress.objects.filter(user=current_user).order_by('id')

    try:

        cart = Cart.objects.get(user=current_user, is_paid=False)

        cart_items = CartItem.objects.filter(cart=cart)

        client = razorpay.Client(auth = (settings.KEY, settings.SECRET))

        payment = client.order.create({'amount' : int(cart.get_grand_total()) * 100, 'currency' : 'INR', 'payment_capture': 1})

    except:

        pass #Just Ignore 
        
    cart.razor_pay_order_id=payment['id']

    cart.save()

    context = {

        'cart': cart,
        'cart_items': cart_items,
        'addresses': addresses,
        'payment' : payment
    }

    return render(request, 'orders/checkout.html', context)





def orderSuccessfully(request):

    order_id = request.GET.get('razorpay_order_id') 

    print('Order id = ',order_id)
    
    cart = Cart.objects.get(user=request.user,razor_pay_order_id=order_id)

    # Payment details storing
    user = request.user

    transaction_id = request.GET.get('razorpay_payment_id')

    cart_total = cart.get_cart_total()

    tax = cart.get_tax()

    grand_total = cart.get_grand_total()

    payment = Payment.objects.create(

        user=user, transaction_id=transaction_id, cart_total=cart_total, tax=tax, grand_total=grand_total
    )

    payment.save()

    # Creating the order in Order table
    delivery_address = userAddress.objects.get(user=request.user,  default=True)

    order = Order.objects.create(

        order_id=order_id, user=user, delivery_address=delivery_address, payment=payment
    )

    # Storing ordered products in OrderItem table
    order_items = CartItem.objects.filter(cart=cart)

    for item in order_items:

        ordered_item = OrderItem.objects.create(

            order=order, product=item.product, item_price=item.get_product_price(), quantity=item.quantity, item_total=item.get_sub_total()
        )

        ordered_item.save()

        if item.variant:

            ordered_item.variant = item.variant.color.color

            ordered_item.save()
            
    # Deleting the cart once it is ordered/paid
    cart.is_paid = False

    cart.delete()

    return render(request, 'orders/orderSuccessfully.html',{'order_id': order_id})





def orders_list(request):

    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders/orders_list.html', {'orders' : orders})





def order_details(request,order_id):

    try:

        order = Order.objects.get(uid=order_id)

        order_items = OrderItem.objects.filter(order=order)


    except:

        pass 

    return render(request, 'orders/order_details.html', {'order_items' : order_items})





def order_tracking(request, item_id):

    current_date = timezone.now()

    item = OrderItem.objects.get(id=item_id)

    context = {

        'item' : item,

        'current_date' : current_date
    }
    return render(request, 'orders/orderTracking.html' ,context)





def order_invoice(request, order_id):

    order = Order.objects.get(uid=order_id,user=request.user)

    order_items = OrderItem.objects.filter(order=order)


    context = {

        'order' : order,
        'order_items' : order_items
    }

    return render(request, 'orders/invoice.html',context)





def cancel_order(request, item_id=None, order_id=None):
        
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))

    order = Order.objects.get(order_id=order_id)

    payment_id = order.payment.transaction_id

    item = OrderItem.objects.get(order=order, id=item_id)

    item_amount = item.item_total * 100


    refund = client.payment.refund(payment_id,{'amount':item_amount})

    return HttpResponse('Payment success')




# Admin Side #

def orderManagement(request):

    context = {

        'orders' : Order.objects.all(),

        'items' : OrderItem.objects.all()

    }
    
    return render(request,'orders/orderManagement.html', context)




