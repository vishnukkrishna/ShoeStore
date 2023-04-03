from django.shortcuts import render, redirect
from store.models import Product, Category, Brand, multipleImage, Variation, Color
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
# Create your views here.


def superadmin_check(user):
    if user.is_authenticated:
        return user.is_superadmin


# Brand Management
@user_passes_test(superadmin_check)
def brandManagement(request):

    dict_brand={

        'brand': Brand.objects.all().order_by('id')
    }

    return render(request, 'productmanagement/brandManagement.html', dict_brand)


# Add Brand
@user_passes_test(superadmin_check)
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
@user_passes_test(superadmin_check)
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
@user_passes_test(superadmin_check)
def deleteBrand(request, id):

    del_brand = Brand.objects.filter(id=id)

    del_brand.delete()

    return redirect(brandManagement)





########################################################################


@user_passes_test(superadmin_check)
def productManagement(request):

    product_dict = {

        'product': Product.objects.all().filter(is_available=True).order_by('id'),

        'category': Category.objects.all(),

        'brand': Brand.objects.all(),
    }

    return render(request, 'productmanagement/productList.html', product_dict)


# Add Product
@user_passes_test(superadmin_check)
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

        p_image = request.FILES['image']

        brand = request.POST['brand']

        category = request.POST['category']


        multi_image = request.FILES.getlist('imagess')

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
                
                if int(stock) < 0:

                    messages.info(request, 'Stock should be a non-negative number')

                    return redirect(addProducts)


        add_product = Product.objects.create(

            title=title,

            slug = slug,

            category=category_instance,

            description=description,

            price=price,

            stock=stock,

            image=p_image,

            brand=brand_instance
        )

        for image in multi_image:

            multipleImage.objects.create(

                product=add_product,

                images=image
            )  

        return redirect(addProducts)

    else:

        return render(request, 'productmanagement/addProducts.html', product_dict)




# Delete Product
@user_passes_test(superadmin_check)
def deleteProduct(request, id):

    del_pro = Product.objects.filter(id=id)

    del_pro.delete()

    return redirect(productManagement)




# Edit Product
@user_passes_test(superadmin_check)
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

        stock = int(request.POST['stock'])

        price = request.POST['price']


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
                
                if stock < 0:

                    messages.info(request, 'Stock should be a non-negative number')

                    return redirect(productManagement)


        edit_pro.update(title=title, description=description, category=category_instance, stock=stock, price=price, brand=brand_instance)

        context = {

            'product': product,

            'category': category
        }
        
        return redirect(productManagement)
    
    else:

        messages.info(request, 'Some fields is empty')

        return render(request, 'productmanagement/productList.html', context)




@user_passes_test(superadmin_check)
def variantsList(request):

    variant = Variation.objects.all()

    color = Color.objects.all()

    product = Product.objects.all()

    context = {

        'variant': variant,
        'color' : color,
        'product': product,

    }

    return render(request, 'productmanagement/addVariants.html', context)





@user_passes_test(superadmin_check)
def addColor(request):

    if request.method == 'POST':

        color = request.POST['color']

        color_add = Color.objects.create(color=color)

        color_add.save()

        return redirect(variantsList)





@user_passes_test(superadmin_check)
def addVariant(request):

    if request.method=='POST':

        color=request.POST['color']

        product=request.POST['product']
        
        try:

            product_instance=Product.objects.get(id=product)

            color_intance=Color.objects.get(id=color)

        except:

            pass


        variant=Variation.objects.create(color=color_intance,product=product_instance)

        variant.save()

        return redirect(variantsList)
    
    else:

        return render(request, 'productmanagement/addVariants.html')


@user_passes_test(superadmin_check)
def editVariant(request, id):

    if request.method == 'POST':

        color = request.POST['color']

        try:

            color_instance = Color.objects.get(id=color)

        except:

            pass


        edit_variant = Variation.objects.filter(id=id)

        edit_variant.update(color=color_instance)

        return redirect(variantsList)
    

    else:

        messages.info(request, 'Some fields is empty')

        return redirect(variantsList)



@user_passes_test(superadmin_check)
def deleteVariant(request,id):

    del_variant = Variation.objects.filter(id=id)

    del_variant.delete()

    return redirect(variantsList)