from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Wishlist,WishlistItem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.



def wishlist(request,wishlist_items=None):

    try:

        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))

        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist,is_active=True)
        
    except ObjectDoesNotExist:

        pass

    context = {       

        'wishlist_items':wishlist_items,
    }
    
    return render(request, 'store/wishlist.html',context)




def _wishlist_id(request):

    wishlist = request.session.session_key

    if not wishlist:

        wishlist = request.session.create()

    return wishlist


def add_wishlist(request,product_id):

    product = Product.objects.get(id=product_id)

    # print(product_id)

    try:

        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))

    except Wishlist.DoesNotExist: 

        wishlist = Wishlist.objects.create( 

            wishlist_id=_wishlist_id(request)

        )

    wishlist.save()  


    try:

        wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist)

        wishlist_item.save()

    except WishlistItem.DoesNotExist:

        wishlist_item = WishlistItem.objects.create(

            product=product,

            wishlist=wishlist
        )

        wishlist_item.save()

    return redirect('wishlist')




def remove_wishlistitem(request,product_id):

    wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))

    product = get_object_or_404(Product,id=product_id)

    wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist)

    wishlist_item.delete()

    return redirect('wishlist')

