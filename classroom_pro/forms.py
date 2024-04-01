from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text='Required. Enter your name.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    role = forms.CharField(max_length=100, help_text='Required. Enter your role.')
    department = forms.CharField(max_length=100, help_text='Enter your department (if applicable).')

    class Meta:
        model = User
        fields = ['name', 'email', 'role', 'department', 'password1', 'password2']
