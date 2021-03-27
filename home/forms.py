from django import forms
from home.models import News


class ImageForm(forms.ModelForm):
    """Form for the image model"""

    class Meta:
        model = News
        fields = ('picture_file',)
