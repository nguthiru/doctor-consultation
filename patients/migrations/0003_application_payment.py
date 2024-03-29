# Generated by Django 3.2 on 2022-09-26 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0004_specialization_consultation_price'),
        ('patients', '0002_alter_patient_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_applied', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
                ('specialization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='doctors.specialization')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_identifier', models.CharField(max_length=100)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.application')),
            ],
        ),
    ]
