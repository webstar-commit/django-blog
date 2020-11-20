# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribe',
            field=models.ManyToManyField(related_name='sub_cat', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
