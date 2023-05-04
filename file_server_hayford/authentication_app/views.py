from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignUp, LoginForm, signUser, passwordChangeView   #dev'ing of models  
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError      #dev'ing of models
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
from django.urls import reverse_lazy

# Create your views here.
@csrf_protect
def index(request):
    return render(request, './filesystem/home.html')


# @__cached__(1 * 60)
@csrf_protect
def signup(request):
    form = UserSignUp
    if request.method == 'POST':
        form = UserSignUp(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = signUser.objects.create_user(email= email, password = password)
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

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = signUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, signUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/')
        
    else:
        return render(request, 'accounts/activation_404.html')

@csrf_protect
def signin(request):
    form = LoginForm(data=request.POST)
    next_url = request.GET.get('next', '')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(reverse_lazy('filesystem:file_list'))
            else:
                return render(request, 'authentication_app/login.html',  {'form': form, 'error': 'Invalid login credentials', 'next': next_url}) 
                
    return render(request, 'authentication_app/login.html', {'form': form, 'next': next_url})


# def signin(request):
#     form = LoginForm(data=dict(request.POST))
#     next_url = request.GET.get('next', '')
#     if request.method == 'POST':
#         form = LoginForm(data=dict(request.POST))
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request=request, email=email, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 if next_url:
#                     return redirect(next_url)
#                 else:
#                     return redirect('filesystem:file_list')
#             else:
#               return render(request, 'authentication_app/login.html',  {'form': form, 'error': 'Invalid login credentials', 'next': next_url}) 
                
#     return render(request, 'authentication_app/login.html', {'form': form, 'next': next_url})



    


def signout(request):
    logout(request)
    return redirect('/')
    

# check if

    

@csrf_protect
def password_Change(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "authentication_app/password_reset/password_reset_email.html"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject=subject, message=c, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("passwordChange/done/")                     
	password_reset_form = PasswordResetForm()
	return render(request, 'authentication_app/password_reset/password_change.html', {'password_reset_form':password_reset_form })
    
#intialization function depending on settings


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
        form = UserRegisterForm()
    return render(request, 'authentication_app/password_reset/password_reset_form.html')


@csrf_protect
def resetPageDone(request):
     return render(request, 'authentication_app/password_reset/password_reset_done.html')


@csrf_protect
def reset_password_confirm(request, uidb64, token):
    try:
        uid =force_str(urlsafe_base64_decode(uidb64))
        user = signUser.objects.get(pf=uid)
    except(signUser.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = passwordChangeView(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data.get('password')
                user.set_password(new_password)
                user.save()
                user =authenticate(request, email=user.email, password=new_password)
                login(request, user)
                
                return render(request, 'authentication_app/password_reset/password_reset_complete.html')
        else:
            form = passwordChangeView()
        return render(request, 'authentication_app/password_reset/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'authentication_app/password_reset/404.html')
