from django import forms
from . import models

# creating a form
class RatingForm(forms.ModelForm):
    class Meta:
        model = models.Rating
        fields = ['rating', 'comment'] # comment 추가하려면 필드안에 'comment'추가
