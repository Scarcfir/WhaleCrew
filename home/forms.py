from django import forms
from home.models import NewsArticle


class ImageForm(forms.ModelForm):
    """Form for the image model"""

    class Meta:
        model = NewsArticle
        fields = ('picture_file',)
