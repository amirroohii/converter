# converter/forms.py

from django import forms
from .models import Image

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

class UploadFileForm(forms.Form):
    file = forms.FileField()