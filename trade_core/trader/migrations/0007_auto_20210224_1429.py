# Generated by Django 3.1.6 on 2021-02-24 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0006_auto_20210222_1247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='unlikes',
        ),
    ]
