# Generated by Django 4.0.3 on 2022-06-04 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_token_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
