from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserSignUp, UserRegisterForm, signUser, passwordChangeView   #dev'ing of models  
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


# Create your views here.
@csrf_protect
def index(request):
    return render(request, './filesystem/home.html')


@csrf_protect
def signin(request):
    form = UserSignUp()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email = email, password = password)
        login(request, user)
        if user == None:
            return HttpResponse("Invalid credentials.")
            
            # return redirect('/')  #watch here again
        else:
            form = UserSignUp()
    return render(request, 'authentication_app/login.html', {'form': form})  
    # return HttpResponse("Valid credentials.")
        


def signout(request):
    logout(request)
    return redirect('/')
    
        
@csrf_protect
def signup(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('firstname')
            last_name = form.cleaned_data.get('lastname')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = signUser.objects.create_user(first_name = first_name, last_name = last_name, username = username, email= email, password = password)
            user.save()
    else:
        form = UserRegisterForm()
    return render(request, 'authentication_app/signup.html', {'form': form})

# check if
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
        return render(request, 'accounts/activation_invalid.html')
    

@csrf_protect
def passwordChange(request):
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
	return render(request, 'reset_pages_template/password_change.html', {'password_reset_form':password_reset_form })
    
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
def passwordChangeDone(request, uidb64, token):
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
