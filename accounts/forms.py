from django.contrib.auth.forms import UserCreationForm
from django import forms as f
from django.contrib.auth.models import User
from . models import Profile

class Usercreate(UserCreationForm):
    email=f.EmailField(required=True)
    class Meta:
        model = User
        fields = ( 'username', 'email', 'password1' ,'password2' )