# Generated by Django 4.0.3 on 2022-06-05 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatlog_student_or_society'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatlog',
            old_name='student_or_society',
            new_name='society_or_student',
        ),
    ]
