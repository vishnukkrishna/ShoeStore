
# from .cart import Cart




# def cart(request):

#     return {'cart': Cart(request)}


from .models import Cart,CartItem
from .views import _cart_id




def counter(request):

    cart_count = 0

    if 'admin' in request.path:

        return {}
    
    else:

        try:

            cart = Cart.objects.filter(cart_id=_cart_id(request))

            # if request.user.is_authenticated:

            #     cart_items = CartItem.objects.all().filter(user=request.user)

            # else:

            cart_items = CartItem.objects.all().filter(cart=cart[:1])

            for cart_item in cart_items:

                cart_count  += 1

        except Cart.DoesNotExist:

            cart_count=0

    return dict(cart_count=cart_count)
