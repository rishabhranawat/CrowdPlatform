# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-09 17:08
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('create_lesson_plan', '0018_auto_20170828_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(default=uuid.uuid1, max_length=2083, unique=True)),
                ('content_hash', models.TextField(default=uuid.uuid1, unique=True)),
            ],
        ),
    ]
