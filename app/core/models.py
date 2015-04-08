from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from xml.etree.ElementTree import ParseError

import xml.etree.cElementTree as et
import os.path

def get_unique_url(instance, filename):
    return os.path.join('pathways', str(instance.user_id.id), filename)

def validate_filefield_file_extension(filefield):
    if not filefield.name.endswith('.xml'):
        raise ValidationError(u'Invalid file format')

class Pathway(models.Model):
    user_id = models.ForeignKey(User)
    pathway_xml = models.FileField(upload_to=get_unique_url, validators=[validate_filefield_file_extension])

class UploadForm(ModelForm):
    def clean(self):
        cleaned_data = super(UploadForm, self).clean()
        _file = cleaned_data.get("pathway_xml")
        if _file is None:
            raise ValidationError(u"File Upload Error")

        contents = _file.read()
        try:
            xml = et.fromstring(contents)
        except:
            raise ValidationError(u"Invalid XML")

    class Meta:
        model = Pathway
        fields = ['pathway_xml',]
