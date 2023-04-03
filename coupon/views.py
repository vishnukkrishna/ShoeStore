from django.shortcuts import render, redirect
from cart.models import Coupon
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from productmanagement.views import superadmin_check
# Create your views here.


@user_passes_test(superadmin_check)
def couponManagement(request):

    context={

        'coupon':Coupon.objects.all()
    }

    return render(request, 'coupon/couponList.html', context)



@user_passes_test(superadmin_check)
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
    



@user_passes_test(superadmin_check)
def edit_coupon(request, id):

    if request.method == 'POST':

        coupon_code = request.POST['coupon_code']

        dis_price = int(request.POST['dis_price'])

        min_amount = int(request.POST['min_amount'])

        try:

            coupon = Coupon.objects.get(id=id)

        except Coupon.DoesNotExist:

            messages.warning(request, 'Oops!Something went wrong')

            return redirect(couponManagement)
        
        if Coupon.objects.filter(coupon_code__iexact=coupon_code).exclude(id=id).exists():

            messages.warning(request, 'Coupon already exists')

            return redirect(couponManagement)
        
        elif dis_price > min_amount :

            messages.warning(request, 'Discount price should be less than minimum amount')

            return redirect(couponManagement)
        
        elif (dis_price or min_amount) <= 0 :

            messages.warning(request, 'Enter a valid discount price/minimum amount')

            return redirect(couponManagement)
        
        
        coupon.coupon_code = coupon_code

        coupon.discount_price = dis_price

        coupon.min_amount = min_amount

        coupon.save()

        messages.success(request, 'Coupon updated succesfully')
        
        return redirect(couponManagement)





@user_passes_test(superadmin_check)
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
    


def coupon_status(request, id):

    try:

        coupon = Coupon.objects.get(id=id)

        if coupon.is_expired:

            coupon.is_expired = False

            coupon.save()

            messages.success(request, f'Coupon {coupon} activated succesfully')

            return redirect(couponManagement)
        
        else:

            coupon.is_expired = True

            coupon.save()

            messages.success(request, f'Coupon {coupon} deactivated succesfully')

            return redirect(couponManagement)
        
    except Coupon.DoesNotExist:

        messages.error(request, 'Oops!Something gone wrong')
        
        return redirect(couponManagement)