from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    personalID = models.CharField(max_length=40)


"""
class Manager(models.Model):
    pass:


class Reservation(models.Model):
    pass:


class Car(models.Model):
    pass:

"""
