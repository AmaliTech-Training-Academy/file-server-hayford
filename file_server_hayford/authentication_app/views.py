from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignUp, LoginForm, UserSignUp, passwordChangeForm  
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail    
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from .models import CustomUser



# Create your views here.
@csrf_protect
def signup(request):
    form = UserSignUp
    if request.method == 'POST':
        form = UserSignUp(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = CustomUser.objects.create_user(email= email, password = password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message=render_to_string('authentication_app/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            message = strip_tags(message)
            mail_subject = 'Activate your account.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail( mail_subject, message, email_from, recipient_list )
            return render(request, 'authentication_app/email_verification.html')
    else:
        form = UserSignUp()
    return render(request, 'authentication_app/signup.html', {'form': form})



#account activation function
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/login/')
        
    else:
        return render(request, 'authentication_app/activation_404.html')



@csrf_protect
def signin(request):
    form = LoginForm(data=request.POST)
    next_url = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if next_url:
                    return render(next_url)
                else:
                    return redirect('filesystem:upload_list')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid login credentials', 'next': next_url})
    return render(request, 'authentication_app/login.html', {'form': form, 'next': next_url})




def signout(request):
    logout(request)
    return redirect('/login/')
     


#intialization function depending on settings
@csrf_protect
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                current_site = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                email_body = render_to_string('authentication_app/password_reset/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                    'protocol': 'http',
                    'site_name': '',
                })
                email_subject = 'Password reset on ' + current_site.domain
                email_body = strip_tags(email_body)
                email = send_mail(email_subject, email_body, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])
                # email.send()
                return render(request, 'authentication_app/password_reset/password_reset_done.html')
                
            except CustomUser.DoesNotExist:
                form.add_error(None, 'Email address not found, try again')
    else:
        form = PasswordResetForm()
    return render(request, 'authentication_app/password_reset/password_reset_form.html', {'form': form})



@csrf_protect
def resetPage(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        newuser = User.objects.create_user( password = password, confirmPassword = confirmPassword)
        try:
            newuser.save()
        except ValueError:
            return HttpResponse('Please go back!')
        
    else:
        form = LoginForm()
    return render(request, 'authentication_app/password_reset/password_reset_form.html')


@csrf_protect
def resetPageDone(request):
     return render(request, 'authentication_app/password_reset/password_reset_done.html')



@csrf_protect
def reset_password_confirm(request, uidb64, token):
    try:
        uid =force_str(urlsafe_base64_decode(uidb64))
        user = UserSignUp.objects.get(pf=uid)
    except(UserSignUp.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = passwordChangeForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data.get('password')
                user.set_password(new_password)
                user.save()
                user =authenticate(request, email=user.email, password=new_password)
                login(request, user)
                
                return render(request, 'authentication_app/password_reset/password_reset_complete.html')
        else:
            form = passwordChangeForm()
        return render(request, 'authentication_app/password_reset/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'authentication_app/password_reset/404.html')
