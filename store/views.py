from django.shortcuts import render,redirect
from . models import Category, Product, Brand, ReviewRating, multipleImage, Variation, Color
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from wishlist.models import WishlistItem, Wishlist
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderItem


# Create your views here.

def store(request):

    all_products = Product.objects.all()

    review = ReviewRating.objects.all()

    if request.GET.get('sortby'):
            
            sort = request.GET.get('sortby')

            if sort == 'new':

                all_products = Product.objects.all().order_by('-created_date')

            elif sort == 'lth':

                all_products = Product.objects.all().order_by('price')

            elif sort == 'htl':
                
                all_products = Product.objects.all().order_by('-price')


    paginator = Paginator(all_products, 8)

    page = request.GET.get('page')

    paged_products = paginator.get_page(page)

    context = {'products': paged_products, 'review': review}

    return render(request, 'store/allproducts.html', context)





def categories(request):

    all_categories = Category.objects.all()

    return {'all_categories': all_categories}





def brands(request):

    all_brands = Brand.objects.all()

    return {'all_brands': all_brands}





def list_category(request, category_slug=None):

    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    paginator = Paginator(products, 4)

    page = request.GET.get('page')

    paged_products = paginator.get_page(page)

    return render(request, 'store/list_category.html', {'category':category, 'products':paged_products})





def list_brand(request, brand_slug=None):

    brand = get_object_or_404(Brand, slug=brand_slug)

    products = Product.objects.filter(brand=brand)

    paginator = Paginator(products, 4)

    page = request.GET.get('page')

    paged_products = paginator.get_page(page)

    return render(request, 'store/list_brand.html', {'brand': brand, 'products': paged_products})





def product_info(request, product_slug):

    in_wishlist = False

    ordered = None

    try:
         

        product = get_object_or_404(Product, slug=product_slug)

        variants = Variation.objects.filter(product=product)

        reviews = ReviewRating.objects.filter(product=product).count()

        if request.user.is_authenticated:

            ordered = OrderItem.objects.filter(product=product, user=request.user).exists()


        context = {

            'product':product,

            'images':multipleImage.objects.filter(product=product),

            'review': ReviewRating.objects.filter(product=product),

            'variants': variants,

            'reviews': reviews,

            'ordered' : ordered,

        }

        if request.GET.get('variant'):
                
                color = request.GET.get('variant')

                variation = Color.objects.get(color=color)

                variant=Variation.objects.get(color=variation,product=product)

                variant_price = product.get_product_price(variation)

                context['in_wishlist'] = in_wishlist

                context.update({

                    'selected_variant': variant,

                    'variant_price': variant_price,

                    'color' : color,
                
                })

        if request.user.is_authenticated:
            
            try:

                wishlist = Wishlist.objects.get(user=request.user)

                in_wishlist = WishlistItem.objects.filter(wishlist=wishlist, product__title=product)

                context['in_wishlist'] = in_wishlist

            except:

                pass

        return render(request, 'store/product_info.html', context)

    except:
         
        return render(request, 'store/product_info.html', context)





def search(request):

    if 'keyword' in request.GET:

        keyword = request.GET['keyword']

        if keyword:

            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(title__icontains=keyword))

            product_count = products.count()


        context = {

            'products': products,
            
            'product_count': product_count,
        }


    return render(request, 'store/allproducts.html', context)




def submit_review(request, product_id):

    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':

        try:

            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)

            form = ReviewForm(request.POST, instance=reviews)

            form.save()

            messages.success(request, 'Thank you! Your review has been updated.')

            return redirect(url)

        except ReviewRating.DoesNotExist:

            form = ReviewForm(request.POST)

            if form.is_valid():

                data = ReviewRating()

                # data.subject = form.cleaned_data['subject']

                data.rating = form.cleaned_data['rating']

                data.review = form.cleaned_data['review']

                data.image = request.FILES.get('image')

                data.ip = request.META.get('REMOTE_ADDR')

                data.product_id = product_id

                data.user_id = request.user.id

                data.save()

                messages.success(request, 'Thank you! Your review has been submitted.')

                return redirect(url)




def deleteReview(request, id):

    del_review = ReviewRating.objects.filter(id=id)

    del_review.delete()

    return redirect(product_info)