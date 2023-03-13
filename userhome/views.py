from django.shortcuts import render, redirect
from .models import userAddress
from .forms import AddressForm
# Create your views here.


def viewAddress(request):

    context = {

        'address':userAddress.objects.filter(user=request.user),
    } 

    return render(request, 'userhome/viewAddress.html', context)



def addAddress(request):

    address = userAddress.objects.filter(user=request.user)

    if request.method == 'POST':

        print(address)
        
        form = AddressForm(request.POST)

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