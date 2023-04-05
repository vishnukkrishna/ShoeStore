from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Wishlist,WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.



# def _wishlist_id(request):

#     wishlist = request.session.session_key

#     if not wishlist:

#         wishlist = request.session.create()

#     return wishlist





@login_required
def wishlist(request,wishlist_items=None):

    try:
        wishlist = Wishlist.objects.get(user=request.user)

        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)

    except:

        pass

    context = {       

        'wishlist_items':wishlist_items,
    }
    
    return render(request, 'store/wishlist.html',context)





@login_required()
def add_wishlist(request,product_id):

    product = Product.objects.get(id=product_id)

    user = request.user
    
    wishlist, _ = Wishlist.objects.get_or_create(user=user)
    wishlist_item= WishlistItem.objects.create(wishlist=wishlist, product=product, quantity=1)
    wishlist_item.save()

    return redirect('wishlist')



@login_required()
def remove_wishlistitem(request,product_id):

    product = Product.objects.get(id=product_id)
    user = request.user

    wishlist = Wishlist.objects.get(user=user)
    wishlist_item = WishlistItem.objects.filter(wishlist=wishlist, product=product)
    wishlist_item.delete()

    return redirect('wishlist')

