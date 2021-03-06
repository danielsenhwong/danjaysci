# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 20:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab_members', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TraineeType',
            new_name='LabPosition',
        ),
        migrations.RemoveField(
            model_name='labmember',
            name='trainee_type',
        ),
        migrations.AddField(
            model_name='labmember',
            name='lab_job_title',
            field=models.ForeignKey(default=1, help_text='The current or last job title the named lab member had in this lab. This is used to track alumni, e.g. Brenda Eustace was a grad student in the lab.', on_delete=django.db.models.deletion.CASCADE, to='lab_members.LabPosition'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='labmember',
            name='current_position',
            field=models.TextField(blank=True, help_text='Leave blank for current members of the lab. For lab alumni, please include current job title along with company/institution/organization information.', null=True),
        ),
    ]
