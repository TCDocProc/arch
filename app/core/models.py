from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
import os.path

def get_unique_url(instance, filename):
	return os.path.join('pathways', str(instance.user_id.id), filename)

class Pathway(models.Model):
	user_id = models.ForeignKey(User)
	pathway_xml = models.FileField(upload_to=get_unique_url)

class UploadForm(ModelForm):
    class Meta:
        model = Pathway
        fields = ['pathway_xml',]