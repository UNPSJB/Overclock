# Generated by Django 3.1.2 on 2020-12-03 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_vendedor_estoyhabilitado'),
    ]

    operations = [
        migrations.AddField(
            model_name='encargado',
            name='bajaEncargado',
            field=models.BooleanField(default=False),
        ),
    ]
