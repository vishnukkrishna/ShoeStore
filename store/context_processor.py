from wishlist.models import Wishlist, WishlistItem
from cart.models import Cart,CartItem



def counter(request):

    wishlist_count = 0

    cart_count = 0

    if request.user.is_authenticated:

        try:

            wishlist = Wishlist.objects.get(user=request.user)

            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)

            for item in wishlist_items:

                wishlist_count += 1

        except Wishlist.DoesNotExist:

            pass

        try:

            cart = Cart.objects.get(user=request.user, is_paid=False)

            cart_items = CartItem.objects.filter(cart=cart)

            for item in cart_items:

                cart_count += 1

        except Cart.DoesNotExist:
            
            pass
    
    return dict(wishlist_count=wishlist_count,cart_count=cart_count)