from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100000)
    file = forms.FileField()