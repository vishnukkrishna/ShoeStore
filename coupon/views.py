from django.shortcuts import render

# Create your views here.



def couponManagement(request):

    return render(request, 'coupon/couponList.html')