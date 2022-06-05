# Generated by Django 4.0.3 on 2022-06-05 04:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('companyname', models.TextField(verbose_name='社名')),
                ('logourl', models.URLField(default='', max_length=512)),
            ],
        ),
    ]