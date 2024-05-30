# Generated by Django 5.0.6 on 2024-05-30 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersTenants', '0008_equipotipo_inventarioequipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id_paciente', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField()),
                ('apellido', models.CharField()),
                ('sexo', models.BinaryField()),
                ('edad', models.IntegerField()),
                ('telefono', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('telefono_emergencia', models.IntegerField()),
            ],
        ),
    ]
