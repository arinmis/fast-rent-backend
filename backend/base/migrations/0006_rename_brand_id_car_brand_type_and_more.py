# Generated by Django 4.0.4 on 2022-05-26 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_rename_transmission_id_car_transmission_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='brand_id',
            new_name='brand_type',
        ),
        migrations.RenameField(
            model_name='car',
            old_name='fuel_id',
            new_name='fuel_type',
        ),
    ]
