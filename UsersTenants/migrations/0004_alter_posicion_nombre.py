# Generated by Django 5.0.6 on 2024-05-29 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersTenants', '0003_alter_empleado_posicion_alter_posicion_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posicion',
            name='nombre',
            field=models.CharField(),
        ),
    ]