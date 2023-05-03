from dataclasses import field
from .models import signUser
from django import forms
from .validator import PasswordValidator

class UserSignUp(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = signUser
        fields = ['email']
        


class UserRegisterForm(forms.ModelForm):
    firstname = forms.CharField(max_length=30, required=True)
    lastname = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', required=True)
    class Meta:
        model = signUser
        fields = ['firstname', 'lastname', 'username', 'email', 'password']
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match')
            
        validator = PasswordValidator()
        validator.validate(password)
        
        return password
    

    def save(self, commit=True):
        user = super(UserSignUp, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.is_active = False
            user.save()
        return user    

class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)


class passwordChangeView(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), label="New Password")
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), label="New Confirm Password")
    class Meta:
        model = signUser
        fields = ['password', 'confirmPassword']


class resetPassword(forms.ModelForm):
    email = forms.EmailField(max_length=244)
    class Meta:
        model = signUser
        fields = ['email']