# Generated by Django 3.2 on 2022-10-08 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='isDoctor',
            new_name='is_doctor',
        ),
    ]