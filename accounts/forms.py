from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email','last_name','first_name', 'password1', 'password2']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['personnage','profile_pic']


