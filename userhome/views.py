from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import userAddress
from .forms import AddressForm
from django.contrib.auth.decorators import login_required
from orders.views import checkOut
from django.contrib import messages
from accounts.views import dashboard
# Create your views here.



@login_required
def addAddress(request, num=0):

    address = userAddress.objects.filter(user=request.user)

    if request.method == 'POST':
        
        form = AddressForm(data=request.POST)

        if form.is_valid():

            address = form.save(commit=False)

            address.user = request.user

            address.save()

            number = int(request.GET.get('num'))
            
            if number == 1:

                return redirect(dashboard)
            
            elif number == 2:

                return redirect(checkOut)
            
        # if form is not valid, add an error message
        else:
            
            messages.error(request, 'Please correct the errors below.')

    else:

        form = AddressForm()

    return render(request,'userhome/addAddress.html', {'form':form, 'num' : num})


@login_required
def editAddress(request, address_id):

    address =userAddress.objects.get(id=address_id)

    if request.method == 'POST':

        form = AddressForm(request.POST, instance=address)

        if form.is_valid():

            form.save()

            return redirect(dashboard)
        
    else:

        form = AddressForm(instance=address)
    
    return render(request, 'userhome/editAddress.html', {'form': form})




@login_required
def deleteAddress(request,address_id,num):

    userAddress.objects.get(id=address_id).delete()

    if num == 1:

        return redirect(dashboard)
    
    elif num == 2:

        return redirect(checkOut)





@login_required       
def default_address(request,address_id,num=0):

    userAddress.objects.filter(user=request.user,default=True).update(default=False)

    userAddress.objects.filter(id=address_id,user=request.user).update(default=True)
         
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
