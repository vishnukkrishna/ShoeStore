from django.shortcuts import render, redirect
from .models import userAddress
from .forms import AddressForm
from django.contrib.auth.decorators import login_required
from orders.views import checkOut
# Create your views here.


def viewAddress(request):

    context = {

        'address':userAddress.objects.filter(user=request.user),
    } 

    return render(request, 'userhome/viewAddress.html', context)



def addAddress(request):

    address = userAddress.objects.filter(user=request.user)

    if request.method == 'POST':
        
        form = AddressForm(data=request.POST)

        if form.is_valid():

            address = form.save(commit=False)

            address.user = request.user

            address.save()

            return redirect(viewAddress)
    else:

        form = AddressForm()

    return render(request,'userhome/addAddress.html', {'form':form})



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



def deleteAddress(request,address_id):

    userAddress.objects.get(id=address_id).delete()

    return redirect(viewAddress)




@login_required       
def default_address(request,address_id,num=0):

    userAddress.objects.filter(user=request.user,default=True).update(default=False)

    userAddress.objects.filter(id=address_id,user=request.user).update(default=True)
         
    return redirect(checkOut)
