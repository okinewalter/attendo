from django import forms
from .models import Record, Station

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['fname', 'lname', 'onames', 'station', 'signature']

    signature = forms.CharField(widget=forms.HiddenInput())  # We'll pass the base64 signature here
