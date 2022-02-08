from django import forms
from .models import UserModel


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['email', 'username']