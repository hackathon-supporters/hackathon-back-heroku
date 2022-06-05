# Generated by Django 4.0.3 on 2022-06-05 04:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('humanprofile', '0002_humanprofile_username_alter_humanprofile_faceurl_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Humanhistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('start_year', models.PositiveSmallIntegerField(verbose_name='start_year')),
                ('start_month', models.PositiveSmallIntegerField(verbose_name='start_month')),
                ('end_year', models.PositiveSmallIntegerField(verbose_name='end_year')),
                ('end_month', models.PositiveSmallIntegerField(verbose_name='end_month')),
                ('role', models.TextField()),
                ('employment_status', models.TextField()),
                ('company_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
