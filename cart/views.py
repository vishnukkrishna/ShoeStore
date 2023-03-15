from django.shortcuts import render, redirect
from .models import Cart, CartItem
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.


def cart_summary(request,total=0,quantity=0,cart_items=None):

    tax=0

    grand_total=0

    try:

        cart_instance =Cart.objects.get(cart_id=_cart_id(request))

        cart_items=CartItem.objects.filter(cart=cart_instance, is_active=True)

        for cart_item in cart_items:

            total +=(cart_item.product.price * cart_item.quantity)

            quantity += cart_item.quantity

        tax=(2*total)/100

        grand_total=total +tax

    except ObjectDoesNotExist:

        pass


    context={

        'total':total,

        'quantity':quantity,

        'cart_item':cart_items,

        'tax':tax,

        'grand_total':grand_total,
    }


    return render(request,"carts/cart_summary.html",context)




def _cart_id(request):

    cart=request.session.session_key

    if not cart:

        cart=request.session.create()

    return cart


@login_required(login_url = 'userlogin')
def add_cart(request,product_id):

    product=Product.objects.get(id=product_id)

    try:

        cart=Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:

        cart=Cart.objects.create(

            cart_id=_cart_id(request)

        )

    cart.save()
    
    try:

        cart_item=CartItem.objects.get(product=product,cart=cart)

        cart_item.quantity +=1 # cart_item.quantity=cart_item.quantity +1

        cart_item.save()

    except CartItem.DoesNotExist:

        cart_item=CartItem.objects.create(

            product=product,

            quantity=1,

            cart=cart,
        )

        cart_item.save()

    return redirect(cart_summary)
    # return render(request,"user_side/cart.html")


# descrease the cart_item

def remove_cart(request,product_id):

    cart=Cart.objects.get(cart_id=_cart_id(request))

    product=get_object_or_404(Product,id=product_id)

    cart_item= CartItem.objects.get(product=product,cart=cart)

    if cart_item.quantity >1:

        cart_item.quantity -=1

        cart_item.save()
    else:
       
       pass

    return redirect(cart_summary)



def remove_cart_item(request,product_id):

    cart=Cart.objects.get(cart_id=_cart_id(request))

    product=get_object_or_404(Product,id=product_id)

    cart_item=CartItem.objects.get(product=product,cart=cart)

    cart_item.delete()

    return redirect(cart_summary)









































# def cart_summary(request):

#     cart = Cart(request)
    
#     return render(request, 'carts/cart_summary.html', {'cart': cart})





# def cart_add(request):

#     cart = Cart(request)

#     if request.POST.get('action') == 'post':

#         product_id = int(request.POST.get('product_id'))

#         product_quantity = int(request.POST.get('product_quantity'))

#         product = get_object_or_404(Product, id=product_id)

#         cart.add(product=product, product_qty=product_quantity)

#         cart_quantity = cart.__len__()

#         response = JsonResponse({'qty': cart_quantity})

#         return response
    




# def cart_delete(request):
    
#     cart = Cart(request)

#     if request.POST.get('action') == 'post':

#         product_id = int(request.POST.get('product_id'))

#         cart.delete(product=product_id)

#         cart_quantity = cart.__len__()

#         cart_total = cart.get_total()

#         response = JsonResponse({'qty':cart_quantity, 'total':cart_total})

#         return response





# def cart_update(request):
    
#     cart = Cart(request)

#     if request.POST.get('action') == 'post':

#         product_id = int(request.POST.get('product_id'))

#         print(product_id)

#         product_quantity = int(request.POST.get('product_quantity'))

#         cart.update(product=product_id, qty=product_quantity)

#         cart_quantity = cart.__len__()

#         cart_total = cart.get_total()

#         response = JsonResponse({'qty':cart_quantity, 'total':cart_total})

#         return response


# def cart_update(request):

#         if request.method == 'POST':

#             prod_id = int(request.POST.get('product_id'))

#             print(prod_id)

#             if(Cart.objects.filter(user=request.user, product_id=prod_id)):

#                 prod_qty = int(request.POST.get('product_qty'))

#                 cart = Cart.objects.get(product_id=prod_id, user=request.user)
                
#                 cart.product_id = prod_qty

#                 cart.save()

#                 return JsonResponse({'status': "No such product found"})
            
#         return redirect(cart_summary)
