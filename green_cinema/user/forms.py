from django import forms
from .models import UserModel
# from .forms import CsRegisterForm



class ProfileForm(forms.Form):
    email = forms.CharField()
    username = forms.CharField()



