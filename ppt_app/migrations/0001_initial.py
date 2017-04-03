# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-02 12:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportOutlineByEditor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('filename', models.CharField(max_length=100)),
                ('outline', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ReportOutlineFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('filename', models.CharField(max_length=100)),
                ('report_outline', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Slide_Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(default='No Name', max_length=100)),
                ('template', models.FileField(default=0, upload_to=b'')),
                ('slug', models.SlugField(max_length=1000, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='reportoutlinefile',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ppt_app.Slide_Template'),
        ),
        migrations.AddField(
            model_name='reportoutlinebyeditor',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ppt_app.Slide_Template'),
        ),
    ]