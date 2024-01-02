from django.shortcuts import render, redirect, get_object_or_404
from store.models import Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from productmanagement.views import superadmin_check

# Create your views here.


# Admin Category List
@user_passes_test(superadmin_check)
def categoryManagement(request):
    dict_category = {"category": Category.objects.all().order_by("id")}

    return render(request, "categorymanagement/categoryList.html", dict_category)


# Add Category
@user_passes_test(superadmin_check)
def addCategory(request):
    if request.method == "POST":
        name = request.POST["name"]

        image = request.FILES["image"]

        slug = request.POST["slug"]

        if Category.objects.filter(name=name).exists():
            messages.info(request, "This category already exists")

            return redirect(categoryManagement)

        else:
            add_category = Category.objects.create(name=name, image=image, slug=slug)

            add_category.save()

            return redirect(categoryManagement)

    else:
        messages.info(request, "Some field is empty")

        return redirect(categoryManagement)


# Edit Category
@user_passes_test(superadmin_check)
def editCategory(request, id):
    product = get_object_or_404(Category, pk=id)

    if request.method == "POST":
        name = request.POST["name"]

        slug = request.POST["slug"]

        try:
            edit_category = Category.objects.get(id=id)

            image = request.FILES["image"]

            edit_category.image = image

            edit_category.save()

        except:
            pass

        if Category.objects.filter(name=name).exists():
            messages.info(request, "Category already exists")

            return redirect(categoryManagement)

        else:
            edit_category = Category.objects.filter(id=id)

            edit_category.update(name=name, slug=slug)

            return redirect(categoryManagement)

    else:
        messages.info(request, "Some fields is empty")

        return render(request, "categorymanagement/categoryList.html")


# Delete Category
@user_passes_test(superadmin_check)
def deleteCategory(request, id):
    delete_cat = Category.objects.filter(id=id)

    delete_cat.delete()

    return redirect(categoryManagement)
