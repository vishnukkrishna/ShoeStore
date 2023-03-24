from django.shortcuts import render, redirect
from cart.models import Coupon
from django.contrib import messages
# Create your views here.



def couponManagement(request):

    context={

        'coupon':Coupon.objects.all()
    }

    return render(request, 'coupon/couponList.html', context)




def add_coupon(request):

    if request.method=='POST':

        coupon_name=request.POST.get('coupon_code')

        discount_price=request.POST.get('discount_price')

        min_amount=request.POST.get('min_amount')

        
        Coupon.objects.create(

            coupon_code=coupon_name,

            min_amount=min_amount, 

            discount_price=discount_price, 
        
        )

        messages.success(request,f'{coupon_name} created successfully')

        return redirect(couponManagement)
    
    else:

        return redirect(couponManagement)
    



def delete_coupon(request):

    if request.method=='POST':

        coupon_id=request.POST.get('coupon_id')

        print('coupon id=',coupon_id)

        try:

            coupon=Coupon.objects.get(id=coupon_id)

            coupon.delete()

            messages.success(request,f'deleted{coupon}successfully')

            return redirect(couponManagement)
        
        except: 
           
           return redirect(couponManagement)
        
    else:

        messages.error(request,f'something went wrong')

        return redirect(couponManagement)