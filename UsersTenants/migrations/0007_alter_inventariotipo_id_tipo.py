# Generated by Django 5.0.6 on 2024-05-30 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersTenants', '0006_inventarioconsumible_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventariotipo',
            name='id_tipo',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
