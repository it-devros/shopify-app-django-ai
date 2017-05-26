# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-24 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=255)),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=127)),
                ('country', models.CharField(max_length=127)),
                ('first_name', models.CharField(max_length=127)),
                ('customer_id', models.CharField(max_length=127)),
                ('last_name', models.CharField(max_length=127)),
                ('phone', models.CharField(max_length=18)),
                ('province', models.CharField(max_length=54)),
                ('zip_code', models.CharField(max_length=10)),
                ('province_code', models.CharField(max_length=5)),
                ('country_code', models.CharField(max_length=5)),
                ('email', models.CharField(max_length=127)),
                ('total_spent', models.CharField(max_length=127)),
                ('created_at', models.CharField(max_length=54)),
                ('updated_at', models.CharField(max_length=54)),
                ('saved_at', models.DateField(auto_now_add=True)),
            ],
        ),
    ]