from django import forms


class UploadFileForm(forms.Form):
    participant_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    registration_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

