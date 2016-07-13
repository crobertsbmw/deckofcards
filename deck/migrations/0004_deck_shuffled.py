# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0003_deck_deck_contents'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='shuffled',
            field=models.BooleanField(default=False),
        ),
    ]
