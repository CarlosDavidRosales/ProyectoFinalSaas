# Generated by Django 5.0.6 on 2024-05-20 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersTenants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='apellido',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='contraseña',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='id_empleado',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='posicion',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='usuario',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
