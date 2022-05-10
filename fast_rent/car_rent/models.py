from django.db import models
from django.contrib.auth.models import User as AuthUser, UserManager

# Create your models here.


class User(AuthUser):
    class Meta:
        db_table = 'User'
    personalID = models.CharField(max_length=15)


"""
class Manager(models.Model):
    pass:


class Reservation(models.Model):
    pass:


class Car(models.Model):
    pass:

"""
