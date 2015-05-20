# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='piles',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
    ]
