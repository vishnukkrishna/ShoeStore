from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.contrib import messages
from store.models import Carousel_Home, Account

# Create your views here.




# Admin HomePage
def index(request):

    if not request.user.is_authenticated:

        return redirect(adminlogin)   
    
    elif not request.user.is_admin:

        return redirect(adminlogin)

    return render(request, 'adminindex.html')




# Admin Login Page
def adminlogin(request):

    if request.user.is_authenticated and request.user.is_superadmin:

        return redirect(index)
    
    if request.method == 'POST':

        email = request.POST['email']

        user_password = request.POST['password']

        user = authenticate(email=email, password=user_password)


        if user is not None :

            if user.is_superadmin:

                auth.login(request, user)

                return redirect(index)
            else:

                messages.info(request, 'You are not an Admin')

                return redirect(adminlogin)
            
        else:

            messages.info(request, 'Invalid login credentials')

            return redirect(adminlogin)
        
    else:

        return render(request, 'adminaccounts/login.html')





# Admin logout Page
def adminlogout(request):

    auth.logout(request)

    messages.success(request, 'You are logged out.')

    return redirect(adminlogin)




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# Admin Banner Page
def bannerList(request):

    context = {

        'banner': Carousel_Home.objects.all().order_by('id')

    }

    return render(request, 'adminaccounts/Banner.html', context)



# Admin Add Banner
def addBanner(request):

    if request.method == 'POST':

        carousel_heading = request.POST['carousel_heading']

        carousel_text = request.POST['carousel_text']

        carousel_img = request.FILES['carousel_img']


        addbanner = Carousel_Home.objects.create(carousel_heading=carousel_heading, carousel_text=carousel_text, carousel_img=carousel_img)

        addbanner.save()

    return redirect(bannerList)




# Delete Banner
def bannerDelete(request,id):

    del_banner = Carousel_Home.objects.filter(id=id)

    del_banner.delete()

    return redirect(bannerList)



# Edit Banner
def editBanner(request,id):
        
    product = get_object_or_404(Carousel_Home, pk=id)

    if request.method == 'POST':

        carousel_heading = request.POST['carousel_heading']

        carousel_text = request.POST['carousel_text']

        try:

            edit_banner = Carousel_Home.objects.get(id=id)

            carousel_img = request.FILES['carousel_img']

            edit_banner.carousel_img = carousel_img

            edit_banner.save()

        except:

            pass

        if Carousel_Home.objects.filter(carousel_heading=carousel_heading).exists():

            messages.info(request, "Banner already exists")

            return redirect(bannerList)
            
        else:

            edit_banner = Carousel_Home.objects.filter(id=id)

            edit_banner.update(carousel_heading=carousel_heading, carousel_text=carousel_text)

            return redirect(bannerList)


    else:

        messages.info(request, "Some fields is empty")

        return render(request, 'adminaccounts/Banner.html')




def adminProfile(request):

    return render(request, 'adminaccounts/adminProfile.html')




def change_admin_password(request, user_id):

    if request.method == 'POST':

        old_password = request.POST['old_password']

        new_password = request.POST['new_password']

        confirm_new_password = request.POST['confirm_new_password']

        user = Account.objects.get(id=user_id)
        
        if not user.check_password(old_password):

            messages.error(request, 'Incorrect password')

            return redirect(adminProfile)
        
        else:

            if new_password == confirm_new_password:

                user.set_password(new_password)
                
                auth.login(request,user)

                messages.success(request, 'Password changed succesfully!')

                return redirect(adminProfile)
            
            else:
                messages.error(request, 'Password doesnot match.')

                return redirect(adminProfile)
            
    return render(request,'adminaccounts/adminProfile.html')





def admin_change_dp(request):

    user_id = request.user.id

    user = Account.objects.get(id=user_id)

    try:

        image = request.FILES['user_image']

        user.user_image=image

        user.save()

    except:

        pass
       
    return redirect(adminProfile)





def admin_profile_edit(request):

    user_id = request.user.id

    if request.method == "POST":

        name = request.POST['name']

        email = request.POST['email']

        update_profile = Account.objects.filter(id=user_id) 

        update_profile.update(first_name=name, email=email)

        messages.success(request, 'updated successfully !!')

        return redirect(adminProfile)

    return render(request, 'adminaccounts/adminProfile.html')
