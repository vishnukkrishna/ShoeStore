from django.shortcuts import render, redirect
from accounts.models import Account
from django.shortcuts import get_object_or_404
# Create your views here.



def userManagement(request):

    user_dict = {

        'userdetails': Account.objects.all().order_by('id'),
    }

    return render(request, 'usermanagement/userManagement.html', user_dict)




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




def editUser(request, id):

    first_name = request.POST['name']

    email = request.POST['email']

    update_user = Account.objects.filter(id=id)

    update_user.update(first_name=first_name, email=email)

    return redirect(userManagement)