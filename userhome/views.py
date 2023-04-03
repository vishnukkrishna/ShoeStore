from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import userAddress
from .forms import AddressForm
from django.contrib.auth.decorators import login_required
from orders.views import checkOut
from django.urls import reverse
# Create your views here.


@login_required
def viewAddress(request):

    context = {

        'address':userAddress.objects.filter(user=request.user),
    } 

    return render(request, 'userhome/viewAddress.html', context)


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

                return HttpResponseRedirect(reverse(viewAddress))
            
            elif number == 2:

                return HttpResponseRedirect(reverse(checkOut))
    else:

        form = AddressForm()

    return render(request,'userhome/addAddress.html', {'form':form, "num" : num})


@login_required
def editAddress(request, address_id):

    address =userAddress.objects.get(id=address_id)

    if request.method == 'POST':

        form = AddressForm(request.POST, instance=address)

        if form.is_valid():

            form.save()

            return redirect(viewAddress)
        
    else:

        form = AddressForm(instance=address)
    
    return render(request, 'userhome/editAddress.html', {'form': form})


@login_required
def deleteAddress(request,address_id):

    userAddress.objects.get(id=address_id).delete()

    return redirect(viewAddress)




@login_required       
def default_address(request,address_id,num=0):

    userAddress.objects.filter(user=request.user,default=True).update(default=False)

    userAddress.objects.filter(id=address_id,user=request.user).update(default=True)
         
    return redirect(checkOut)
