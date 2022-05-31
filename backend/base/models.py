from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    pass

"""
NOTE: user types 
    Normal user: is_staff=False, is_superuser=False
    Staff user (can access the admin interface): is_staff=True
    Super user (can do everything): is_superuser=True
"""

class Customer(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 citizen_id = models.CharField(max_length=15)


# types are constant values stored in DB
class TransmissionType(models.Model):
    transmission_type = models.CharField(max_length=20)

class BrandType(models.Model):
    brand_type = models.CharField(max_length=20)


class FuelType(models.Model):
    fuel_type = models.CharField(max_length=20)

class Location(models.Model):
    city = models.CharField(max_length=60)
    address_desc = models.CharField(max_length=150)

class Car(models.Model):
     transmission_type = models.ForeignKey(TransmissionType, on_delete=models.PROTECT)
     brand_type = models.ForeignKey(BrandType, on_delete=models.PROTECT)
     fuel_type  = models.ForeignKey(FuelType, on_delete=models.PROTECT)
     location = models.ForeignKey(Location, on_delete=models.PROTECT)
     photo = models.ImageField(upload_to='cars')
     daily_price = models.IntegerField()
     allocated_by = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.PROTECT)
     is_reserved = models.BooleanField(default=False)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    pickup_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='pickup_location')
    return_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='return_location')
    pickup_date = models.DateField()   
    return_date = models.DateField()   
    is_active = models.BooleanField(default=True);

class Rent(models.Model):
    reservation_id = models.OneToOneField(Reservation, on_delete=models.PROTECT)
