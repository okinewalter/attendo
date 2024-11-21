# Generated by Django 5.1.3 on 2024-11-19 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('station', '0002_alter_station_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('onames', models.CharField(blank=True, max_length=100)),
                ('time_in', models.DateTimeField(auto_now_add=True)),
                ('time_out', models.DateTimeField()),
                ('signature', models.ImageField(blank=True, null=True, upload_to='signatures/')),
                ('station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='station.station')),
            ],
        ),
    ]
