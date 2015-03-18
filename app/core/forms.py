from django import forms
from models import Pathway

class UploadPathwayForm(forms.Form):
    xmlfile = forms.FileField(
        label='Select a file'
    )