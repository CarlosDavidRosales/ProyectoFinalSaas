# Generated by Django 5.0.6 on 2024-05-30 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersTenants', '0009_paciente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='sexo',
            field=models.CharField(),
        ),
    ]
