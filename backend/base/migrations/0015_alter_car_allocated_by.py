# Generated by Django 4.0.4 on 2022-05-30 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_rename_is_allocated_car_allocated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='allocated_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]