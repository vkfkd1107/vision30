from django import forms
from .models import FileUpload

# class UploadFileForm(forms.Form):
#     title=forms.CharField(max_length=50)
#     file=forms.FileField()

class UploadForm(forms.ModelForm):
    
    class Meta:
        model = FileUpload
        fields = {"pic"}

