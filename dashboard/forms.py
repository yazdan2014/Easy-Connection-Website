from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class SignupUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'role')