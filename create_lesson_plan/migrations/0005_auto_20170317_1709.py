# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-17 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_lesson_plan', '0004_lesson_stage'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='num_vote_down',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='lesson',
            name='num_vote_up',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='lesson',
            name='vote_score',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
