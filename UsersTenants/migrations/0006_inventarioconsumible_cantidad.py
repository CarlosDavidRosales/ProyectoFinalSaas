# Generated by Django 5.0.6 on 2024-05-30 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersTenants', '0005_inventariotipo_inventarioconsumible'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventarioconsumible',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
    ]
