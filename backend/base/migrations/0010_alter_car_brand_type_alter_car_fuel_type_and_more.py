# Generated by Django 4.0.4 on 2022-05-27 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_reservation_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='brand_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.brandtype'),
        ),
        migrations.AlterField(
            model_name='car',
            name='fuel_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.fueltype'),
        ),
        migrations.AlterField(
            model_name='car',
            name='transmission_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.transmissiontype'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='reservation_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='base.reservation'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.car'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pickup_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pickup_location', to='base.location'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='return_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='return_location', to='base.location'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]