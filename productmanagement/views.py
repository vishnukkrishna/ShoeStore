from django.shortcuts import render, redirect
from store.models import Product, Category, Brand
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.



# Brand Management
def brandManagement(request):

    dict_brand={

        'brand': Brand.objects.all().order_by('id')
    }

    return render(request, 'productmanagement/brandManagement.html', dict_brand)


# Add Brand
def addBrand(request):

    if request.method == 'POST':

        name = request.POST['name']

        image = request.FILES['image']

        slug=request.POST['slug']

        if Brand.objects.filter(name=name).exists():

            messages.info(request,"This brand already exists")

            return redirect(brandManagement)
        
        else:

            add_brand = Brand.objects.create(name=name, image=image, slug=slug)

            add_brand.save()

            return redirect(brandManagement)


    else:

        messages.info(request,'Some field is empty')

        return redirect(brandManagement)



# Edit Brand
def editBrand(request, id):

    product = get_object_or_404(Brand, pk=id)

    if request.method == 'POST':

        name = request.POST['name']

        slug = request.POST['slug']

        try:

            edit_brand = Brand.objects.get(id=id)
            
            image = request.FILES['image']

            edit_brand.image=image

            edit_brand.save()

        except:

            pass

        if Brand.objects.filter(name=name).exists():

            messages.info(request, "Brand already exists")

            return redirect(brandManagement)
        
        else:

            edit_brand = Brand.objects.filter(id=id)

            edit_brand.update(name=name, slug=slug)

            return redirect(brandManagement)
        

    else:

        messages.info(request, 'Some fields is empty')

        return render(request, 'productmanagement/brandManagement.html')



# Delete Brand
def deleteBrand(request, id):

    del_brand = Brand.objects.filter(id=id)

    del_brand.delete()

    return redirect(brandManagement)



########################################################################



def productManagement(request):

    product_dict = {

        'product': Product.objects.all().filter(is_available=True).order_by('id'),

        'category': Category.objects.all(),

        'brand': Brand.objects.all(),
    }

    return render(request, 'productmanagement/productList.html', product_dict)


# Add Product
def addProducts(request):

    product_dict = {

        'category': Category.objects.all(),

        'brand': Brand.objects.all(),

    }

    if request.method == 'POST':

        title = request.POST['title']

        slug=request.POST['slug']

        description = request.POST['description']

        price = request.POST['price']

        stock = request.POST['stock']

        image = request.FILES['image']

        brand = request.POST['brand']

        category = request.POST['category']

        color = request.POST['color']

        category_instance = Category.objects.get(id=category)

        brand_instance = Brand.objects.get(id=brand)

        check = [price, stock]

        for values in check:

            if values == '':

                messages.info(request, 'Some fields are empty')

                return redirect(addProducts)
            
            else:

                pass

            try:

                check_number = int(price)

                check_number = int(stock)

            except:

                messages.info(request,'Number field got unexpected values')

                return redirect(addProducts)
            
            try:

                check_pos = [int(price), int(stock)]

            except ValueError:

                messages.info(request, 'Price and stock must be valid integers')

                return redirect(addProducts)
            
            for value in check_pos:

                if int(price) < 0:

                    messages.info(request, 'Price should be a positive number')

                    return redirect(addProducts)

        add_product = Product.objects.create(

            title=title,

            slug = slug,

            category=category_instance,

            description=description,

            color=color,

            price=price,

            stock=stock,

            image=image,

            brand=brand_instance
        )

        
        add_product.save()

        return redirect(addProducts)

    else:

        return render(request, 'productmanagement/addProducts.html', product_dict)




# Delete Product
def deleteProduct(request, id):

    del_pro = Product.objects.filter(id=id)

    del_pro.delete()

    return redirect(productManagement)




# Edit Product
def editProduct(request, id):

    product = get_object_or_404(Product, pk=id)

    category = Category.objects.all()

    if request.method == 'POST':

        try:

            edit_pro = Product.objects.get(id=id)

            image = request.FILES['image']

            edit_pro.image = image

            edit_pro.save()

        except:

            pass

        title = request.POST['title']

        description = request.POST['description']

        category = request.POST['category']

        brand = request.POST['brand']

        stock = request.POST['stock']

        price = request.POST['price']

        color = request.POST['color']

        brand_instance = Brand.objects.get(id=brand)

        category_instance = Category.objects.get(id=category)


        edit_pro = Product.objects.filter(id= id)

        check = [price, stock]

        for values in check:

            if values == '':

                messages.info(request, 'Some fields are empty')

                return redirect(productManagement)
            
            else:

                pass

            try:

                check_number = int(price)

                check_number = int(stock)

            except:

                messages.info(request,'Number field got unexpected values')

                return redirect(productManagement)
            
            try:

                check_pos = [int(price), int(stock)]

            except ValueError:

                messages.info(request, 'Price and stock must be valid integers')

                return redirect(productManagement)
            
            for value in check_pos:

                if int(price) < 0:

                    messages.info(request, 'Price should be a positive number')

                    return redirect(productManagement)



        edit_pro.update(title=title, description=description, category=category_instance, stock=stock, price=price, color=color, brand=brand_instance)

        context = {

            'product': product,

            'category': category
        }
        
        return redirect(productManagement)
    
    else:

        messages.info(request, 'Some fields is empty')

        return render(request, 'productmanagement/productList.html', context)
