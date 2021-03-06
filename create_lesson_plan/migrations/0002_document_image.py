# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 18:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('create_lesson_plan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to=b'documents')),
                ('lesson_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create_lesson_plan.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to=b'images')),
                ('lesson_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create_lesson_plan.lesson')),
            ],
        ),
    ]
