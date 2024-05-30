# Generated by Django 5.0.6 on 2024-05-30 09:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersTenants', '0014_consulta_finalizada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulta',
            name='dentista',
            field=models.ForeignKey(default='ELIMINADO', on_delete=django.db.models.deletion.SET_DEFAULT, to='UsersTenants.empleado'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='procedimiento',
            field=models.ForeignKey(default='ELIMINADO', on_delete=django.db.models.deletion.SET_DEFAULT, to='UsersTenants.procedimiento'),
        ),
    ]
