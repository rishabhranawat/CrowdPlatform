# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-28 18:38
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('create_lesson_plan', '0017_testscore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offlinedocument',
            name='link',
            field=models.CharField(default=uuid.uuid1, max_length=600, unique=True),
        ),
    ]
