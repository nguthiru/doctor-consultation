# Generated by Django 3.2 on 2022-11-12 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0013_auto_20221017_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]
