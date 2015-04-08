# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150311_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathway',
            name='pathway_xml',
            field=models.FileField(upload_to=core.models.get_unique_url, validators=[core.models.validate_filefield_file_extension]),
            preserve_default=True,
        ),
    ]
