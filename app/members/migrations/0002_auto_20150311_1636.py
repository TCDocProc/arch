# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathway',
            name='pathway_xml',
            field=models.FileField(upload_to=members.models.get_unique_url),
            preserve_default=True,
        ),
    ]
