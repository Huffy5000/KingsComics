from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import AuthenticationForm,UsernameField

from .models import CustomUser

class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'register_username_input form-input', 'id' :'register_username_id','placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'register_email_input form-input', 'id' :'register_email_id','placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'register_password1_input form-input', 'id' :'register_password1_id','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'register_password2_input form-input', 'id' :'register_password2_id','placeholder':'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        labels = {
            'username':'Username',
            'email':'Email',
            'password1':'Password',
            'password2':'Confirm Password',
        }
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        
        
class LoginForm(AuthenticationForm):
    
    def __init__(self, request: Any = ..., *args: Any, **kwargs: Any) -> None:
        super(LoginForm,self).__init__(request, *args, **kwargs)
        
    username = UsernameField(widget=forms.TextInput(
        attrs={'class':'form-control login-username-input','placeholder':'Username'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs = {'class':'form-control login-password-input','placeholder':'Password'}
    ))




class forgotPasswordEmailVal(PasswordResetForm):
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email__iexact = email, is_active = True).exists():
            msg = ("There is no user registered with the specified email adress.")
            self.add_error('email',msg)
        return email 
    
    
