# Generated by Django 4.0.4 on 2022-05-26 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_rename_pickup_location_id_reservation_pickup_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
