from django.contrib import admin
from .models import * 
"""
                   User, Customer, TranmissionType, BrandType
                   FuelType, Car, Location, Reservation, 
                   Reservation, Rent
"""

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(TransmissionType)
admin.site.register(BrandType)
admin.site.register(FuelType)
admin.site.register(Car)
admin.site.register(Location)
admin.site.register(Reservation)
admin.site.register(Rent)
