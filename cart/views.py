from django.shortcuts import render, redirect
from .models import Cart, CartItem, Coupon
from store.models import Product, Variation, Color
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.


# this is a private method where our session id is stored

@login_required
def cart_summary(request):

    cart=None

    cart_items=None

    coupon = Coupon.objects.all()

    try:

        cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)

        print(cart)

        print('Loading')


        cart_items=CartItem.objects.filter(cart=cart, is_active=True)


    except Exception as e:

        print(e)

    if request.method=='POST':

        coupon = request.POST.get('coupon')

        coupon_obj=Coupon.objects.filter(coupon_code__icontains=coupon)

        if not coupon_obj.exists():

            messages.error(request,'invalid Coupon')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        
        if cart.coupon:

            messages.warning(request, 'Coupon Already applied')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart.get_cart_total() < coupon_obj[0].min_amount:

            messages.warning(

                request, f'Total amount should be greater than ₹{coupon_obj[0].min_amount} excluding tax')
            
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon_obj[0].is_expired:
             
             messages.warning(request, 'This coupon has expired')

             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        cart.coupon = coupon_obj[0]

        cart.save()

        messages.success(request, 'Coupon Applied')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    context = {

        'cart_items': cart_items,
        'cart': cart,
        'coupon':coupon,
    }

    return render(request,"carts/cart_summary.html",context)




@login_required
def add_cart(request,product_id):

    product_variant = None

    try:
   
        variation = request.GET.get('variant')

        color = Color.objects.get(color=variation)
       
        product = Product.objects.get(id=product_id)

        user = request.user

        if color:

            product_variant = Variation.objects.get(product=product, color=color)

      
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
       

        is_cart_item = CartItem.objects.filter(

            cart=cart, product=product, variant=product_variant

        ).exists()
        
        

        if is_cart_item:

            cart_item = CartItem.objects.get(

                cart=cart, product=product, variant=product_variant
            )

            if cart_item.quantity >= product.stock:

                messages.warning(request, "Sorry, the product is out of stock.")
                
                return redirect(cart_summary)
            
            cart_item.quantity += 1

            cart_item.save()

        else:

            cart_item = CartItem.objects.create(

                product=product, quantity=1, cart=cart, variant=product_variant
            )

            cart_item.save()

    except:

        pass


    return redirect(cart_summary)




def remove_cart(request,product_id,cart_item_id):
    
    try:

        product = Product.objects.get(id=product_id)

        cart = Cart.objects.get(user=request.user, is_paid=False)

        cart_item = CartItem.objects.get(

            product=product, id=cart_item_id, cart=cart
        )

        if cart_item.quantity > 1:
            
            cart_item.quantity -= 1

            cart_item.save()

        else:
          
            pass

    except:

        pass


    return redirect(cart_summary)





def remove_cart_item(request,product_id,cart_item_id):

    product = Product.objects.get(id=product_id)

    cart = Cart.objects.get(user=request.user, is_paid=False)

    cart_item = CartItem.objects.filter(

        product=product, id=cart_item_id, cart=cart
    )
    
    cart_item.delete()

    return redirect(cart_summary)




def remove_coupon(request):

    try:

        cart = Cart.objects.get(user=request.user,is_paid=False)

        cart.coupon = None

        cart.save()

        messages.success(request, 'Coupon removed successfully')

    except:

        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))







































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
