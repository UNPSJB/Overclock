# Generated by Django 4.2.2 on 2023-06-29 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_provincia_nombre'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='localidad',
            unique_together={('nombre', 'provincia')},
        ),
    ]