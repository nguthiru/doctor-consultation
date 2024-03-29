# Generated by Django 3.2 on 2022-10-04 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_auto_20220926_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False)),
                ('payment_identifier', models.CharField(max_length=100)),
                ('completed', models.BooleanField(default=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.application')),
            ],
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
