# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathway',
            name='pathway_xml',
            field=models.FileField(upload_to=core.models.get_unique_url),
            preserve_default=True,
        ),
    ]
