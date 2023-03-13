from django.shortcuts import render,redirect
from . models import Category, Product, Brand, ReviewRating, multipleImage
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.models import CartItem
from cart.views import _cart_id
from accounts.models import Account
from .forms import ReviewForm
from django.contrib import messages


# Create your views here.

def store(request):

    all_products = Product.objects.all()

    paginator = Paginator(all_products, 8)

    page = request.GET.get('page')

    paged_products = paginator.get_page(page)

    context = {'products': paged_products}

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

    product = get_object_or_404(Product, slug=product_slug)

    in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()

    context = {

        'product':product,

        'in_cart':in_cart,

        'images':multipleImage.objects.filter(product=product),
    }

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





def orderSuccessfully(request):

    return render(request, 'orders/orderSuccessfully.html')





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

                data.subject = form.cleaned_data['subject']

                data.rating = form.cleaned_data['rating']

                data.review = form.cleaned_data['review']

                data.ip = request.META.get('REMOTE_ADDR')

                data.product_id = product_id

                data.user_id = request.user.id

                data.save()

                messages.success(request, 'Thank you! Your review has been submitted.')

                return redirect(url)

