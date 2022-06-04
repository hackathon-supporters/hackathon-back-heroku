# Generated by Django 4.0.3 on 2022-06-04 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humanprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='humanprofile',
            name='username',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='humanprofile',
            name='faceurl',
            field=models.URLField(default='', max_length=512, verbose_name='faceurl'),
        ),
        migrations.AlterField(
            model_name='humanprofile',
            name='society_or_student',
            field=models.BooleanField(default=False, help_text='社会人か就活生か'),
        ),
    ]
