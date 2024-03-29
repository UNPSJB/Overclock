# Generated by Django 3.1.1 on 2020-09-18 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_auto_20200918_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=800)),
                ('email', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=200)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.categoria')),
                ('localidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.localidad')),
                ('servicios', models.ManyToManyField(to='core.Servicio')),
            ],
        ),
        migrations.CreateModel(
            name='TemporadaAlta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('inicio', models.DateField()),
                ('fin', models.DateField()),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='PrecioPorTipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baja', models.DecimalField(decimal_places=2, max_digits=20)),
                ('alta', models.DecimalField(decimal_places=2, max_digits=20)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tipohabitacion')),
            ],
        ),
        migrations.CreateModel(
            name='PaqueteTuristico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('coeficiente', models.DecimalField(decimal_places=2, max_digits=3)),
                ('inicio', models.DateField()),
                ('fin', models.DateField()),
                ('habitaciones', models.ManyToManyField(to='hotel.Habitacion')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
        ),
        migrations.AddField(
            model_name='hotel',
            name='tipos',
            field=models.ManyToManyField(through='hotel.PrecioPorTipo', to='core.TipoHabitacion'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='vendedores',
            field=models.ManyToManyField(to='core.Vendedor'),
        ),
        migrations.AddField(
            model_name='habitacion',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habitaciones', to='hotel.hotel'),
        ),
        migrations.AddField(
            model_name='habitacion',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tipohabitacion'),
        ),
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_habitaciones', models.PositiveSmallIntegerField()),
                ('coeficiente', models.DecimalField(decimal_places=2, max_digits=3)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
        ),
    ]
