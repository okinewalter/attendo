# Generated by Django 5.1.3 on 2024-11-19 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
