from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect


from store.models import Carousel_Home, Brand
from store .models import Product
from .models import Account
from . forms import RegistrationForm
from userhome.models import userAddress


# Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.


# Website Home Page
def home(request):

    all_products = Product.objects.all()

    context = {

        'products': all_products,

        'banner':Carousel_Home.objects.all().order_by('id'),

        'all_brands':Brand.objects.all(),

    }
    return render(request,'userindex.html',context)   




# User Registration
def register(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data['first_name']

            last_name = form.cleaned_data['last_name']

            email = form.cleaned_data['email']

            phone_number = form.cleaned_data['phone_number']

            password = form.cleaned_data['password']

            username = email.split("@")[0]

            
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)

            user.phone_number = phone_number
            
            user.save()


            # User Activation

            current_site = get_current_site(request)

            mail_subject = 'Please activate your account'

            message = render_to_string('accounts/account_verification_email.html', {

                'user': user,

                'domain': current_site,

                'uid': urlsafe_base64_encode(force_bytes(user.pk)),

                'token': default_token_generator.make_token(user),

            })

            to_email = email

            send_email = EmailMessage(mail_subject, message, to=[to_email])

            send_email.send()


            messages.success(request, "Thank you for registering with us. We have sent you a verification email to your email address. Please verify it.")

            return redirect(register)


    else:

        form = RegistrationForm()


    context = {
        'form': form,
    }

    return render(request, 'accounts/signuppage.html', context)



# User Login
def userlogin(request):

    if request.user.is_authenticated:

        return redirect(home)

    if request.method == 'POST':

        email = request.POST['email']

        password = request.POST['password']


        user = auth.authenticate(email=email, password=password)


        if user is not None:

            auth.login(request, user)

            print(request.path_info)

            return HttpResponseRedirect(request.path_info)
        
        else:
            
            messages.error(request, 'Invalid login credentials')

            return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/loginpage.html')





# User Logout
@login_required(login_url = 'userlogin')
def userlogout(request):

    auth.logout(request)

    messages.success(request, 'You are logged out.')

    return redirect(userlogin)



# Account Activiate
def activate(request, uidb64, token):

    try:

        uid = urlsafe_base64_decode(uidb64).decode()

        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):

        user = None


    if user is not None and default_token_generator.check_token(user, token):

        user.is_active = True

        user.save()

        messages.success(request, 'Congratulations! Your account is now activeed')

        return redirect(userlogin)
    
    else:

        messages.error(request, 'Invalid activation link')

        return redirect(register)






# Forgot Password
def forgotPassword(request):

    if request.method == 'POST':

        email = request.POST['email']

        if Account.objects.filter(email=email).exists():

            user = Account.objects.get(email__exact=email)



            # Reset password email
            current_site = get_current_site(request)

            mail_subject = 'Reset Your Password'

            message = render_to_string('accounts/reset_password_email.html', {

                'user': user,

                'domain': current_site,

                'uid': urlsafe_base64_encode(force_bytes(user.pk)),

                'token': default_token_generator.make_token(user),

            })

            to_email = email

            send_email = EmailMessage(mail_subject, message, to=[to_email])

            send_email.send()

            messages.success(request, 'Password reset eamil has been sent to your email address.')

            return redirect(userlogin)


        else:

            messages.error(request, 'Account does not exist!')

            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')



# Resets password Validation
def resetpassword_validate(request, uidb64, token):

    try:

        uid = urlsafe_base64_decode(uidb64).decode()

        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):

        user = None


    if user is not None and default_token_generator.check_token(user, token):

        request.session['uid'] = uid

        messages.success(request, 'Please reset your password')

        return redirect(resetPassword)
    
    else:

        messages.error(request, 'This link has been expired. Please try again')

        return redirect(userlogin)
    



# Reset Password
def resetPassword(request):

    if request.method == 'POST':

        password = request.POST['password']

        confirm_password = request.POST['confirm_password']


        if password == confirm_password:

            uid = request.session.get('uid')

            user = Account.objects.get(pk=uid)

            user.set_password(password)

            user.save()

            messages.success(request, 'Password reset successful')

            return redirect(userlogin)


        else:

            messages.error(request, 'Password do not match')

            return redirect(resetPassword)
        
    else:

        return render(request, 'accounts/resetPassword.html')
    



# User dashboard
@login_required(login_url = 'userlogin')
def dashboard(request):

    context = {

        'address':userAddress.objects.filter(user=request.user),
    } 

    return render(request, 'accounts/dashboard.html', context)




# User Profile Edit
@login_required(login_url = 'userlogin')
def edit_profile(request, user_id):

    if request.method == 'POST':

        first_name = request.POST['first_name']

        last_name = request.POST['last_name']

        phone_number = request.POST['phone_number']

        edited_user = Account.objects.filter(id=user_id)

        edited_user.update(first_name=first_name, last_name=last_name, phone_number=phone_number)

        messages.success(request,'Profile Details updated successfully')

        return redirect(dashboard)
    
    return render(request, 'accounts/edit_profile.html')




# User profile Password Change
@login_required(login_url = 'userlogin')
def change_password(request, user_id):

    if request.method == 'POST':

        old_password = request.POST['old_password']

        new_password = request.POST['new_password']

        confirm_new_password = request.POST['confirm_new_password']

        user = Account.objects.get(id=user_id)

        if not user.check_password(old_password):

            messages.error(request, 'Incorrect password')

            return redirect(dashboard)
        
        else:

            if new_password == confirm_new_password:

                user.set_password(new_password)

                user.save()

                # auth.login(request,user)

                messages.success(request, 'Password changed succesfully!Please login again!')

                return redirect(userlogin)
            
            else:

                messages.error(request, 'Password doesnot match.')

                return redirect(dashboard)
            
    return render(request,'accounts/change_password.html')




# User Profile DP change
@login_required(login_url = 'userlogin')
def change_dp(request):

    user_id = request.user.id

    user = Account.objects.get(id=user_id)

    try:
        
        image = request.FILES['user_image']

        user.user_image = image

        user.save()

    except:

        pass

    return redirect(dashboard)




