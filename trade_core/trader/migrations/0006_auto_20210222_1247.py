# Generated by Django 3.1.6 on 2021-02-22 10:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trader', '0005_auto_20210222_1235'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postslikes',
            unique_together={('post', 'user')},
        ),
    ]