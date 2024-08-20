from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 

class UserRegistrationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=CustomUser.ACCOUNT_TYPE)
    email=forms.EmailField(max_length=100)
    phone=forms.CharField(max_length=100)
    class Meta:
        model = CustomUser
        fields = ('username', 'email','phone','password1', 'password2', 'account_type')
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }



