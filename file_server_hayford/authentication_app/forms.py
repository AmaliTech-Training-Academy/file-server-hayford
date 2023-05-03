from dataclasses import field
from .models import signUser
from django import forms

class UserformAPI(forms.ModelForm):
    password = forms.CharField()
    
    class Meta:
        model = signUser
        fields = ['email','password']
        


class UserRegisterAPI(forms.ModelForm):
    password = forms.CharField()
    firstname = forms.CharField(max_length=30, required=True)
    lastname = forms.CharField(max_length=30, required=True)
    class Meta:
        model = signUser
        fields = ['firstname', 'lastname', 'username', 'email', 'password']
        

class StudentForm(forms.ModelForm):
    password = forms.CharField()


class passwordChangeView(forms.ModelForm):
    password = forms.CharField()
    confirmPassword = forms.CharField()
    class Meta:
        model = signUser
        fields = ['password', 'confirmPassword']


class resetPassword(forms.ModelForm):
    email = forms.EmailField(max_length=244)
    class Meta:
        model = signUser
        fields = ['email']