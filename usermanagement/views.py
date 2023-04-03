from django.shortcuts import render, redirect
from accounts.models import Account
from store.models import ReviewRating
from django.shortcuts import get_object_or_404
from django.contrib import messages
from productmanagement.views import superadmin_check
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

@login_required
@user_passes_test(superadmin_check)
def userManagement(request):

    user_dict = {

        'userdetails': Account.objects.all().order_by('id'),
    }

    return render(request, 'usermanagement/userManagement.html', user_dict)




@login_required
@user_passes_test(superadmin_check)
def blockUnblock(request, id):

    user=get_object_or_404(Account,id=id)

    if user.is_active:

        user.is_active=False

        user.save()

        return redirect(userManagement)
    
    else:

        user.is_active=True

        user.save()

        return redirect(userManagement)



@login_required
@user_passes_test(superadmin_check)
def editUser(request, id):

    first_name = request.POST['name']

    email = request.POST['email']

    update_user = Account.objects.filter(id=id)

    update_user.update(first_name=first_name, email=email)

    return redirect(userManagement)





# Review Management #


def review_management(request):

    reviews = ReviewRating.objects.all()

    return render(request, 'usermanagement/reviewManagement.html', {'reviews' : reviews})





def remove_review(request, id):

    try:

        review = ReviewRating.objects.get(id=id)

        review.delete()

        messages.success(request, 'Review removed succesfully')

        return redirect(review_management)
    
    except ReviewRating.DoesNotExist:

        messages.warning(request, 'Oops!Something went wrong')

        return redirect(review_management)