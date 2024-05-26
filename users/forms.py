from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100, required=True)
    personal_number = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'personal_number', 'date_of_birth', 'password1', 'password2']
