# Generated by Django 3.2 on 2022-10-17 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0010_auto_20221017_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='identifier',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]