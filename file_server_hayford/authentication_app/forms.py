from .models import CustomUser
from django import forms
from .validator import PasswordValidator
from django.contrib.auth.forms import AuthenticationForm


class UserSignUp(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password', required=True)
    class Meta:
        model = CustomUser
        fields = [ 'email', 'password']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match')
        validator = PasswordValidator()
        validator.validate(password)
        return password
    
#function to set user to false until account is verified
    def save(self, commit=True):
        user = super(UserSignUp, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.is_active = False
            user.save()
        return user    
        

class passwordChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), label="New Password")
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), label="New Confirm Password")
    class Meta:
        model = CustomUser
        fields = []

class LoginForm(AuthenticationForm):
    pass

