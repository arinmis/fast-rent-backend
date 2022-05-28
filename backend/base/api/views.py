from django.http import JsonResponse 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from .utils import epochToDate, deallocate_car
from itertools import chain
from django.db.models import Q
from threading import Timer
from . import serializers
import datetime
import base.models as models

# customize acces tokens
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
            '/api/token',
            '/api/token/refresh',
            ]
    return Response(routes)




@api_view(['GET', "PUT"])
@permission_classes([IsAuthenticated])
def customer(request, id):
    customer  = models.Customer.objects.filter(user_id=id) 

    if request.method == 'GET':
        serializer = serializers.CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = serializers.CustomerSerializer(data=request.data)
        # skip validation for now: https://stackoverflow.com/questions/60533893/user-with-this-username-already-exists-in-drf-modelserializer-if-not-specified
        if serializer.is_valid() or True:
            serializer.update(customer[0], serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_customer(request):
    serializer = serializers.CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rent_locations(request):
    location = models.Location.objects.all()
    serializer = serializers.LocationSerializer(location, many=True)
    return Response(serializer.data)


@api_view(['GET', "POST"])
@permission_classes([IsAuthenticated])
def car(request):
    if request.method == "GET":
        cars = models.Car.objects.all()
        serializer = serializers.CarSerializer(cars, many=True, context={"request": request})
        return Response(serializer.data)
    elif request.method == "POST":
        # cars that are rented given range
        cars_busy = models.Reservation.objects.filter(
                   (Q(pickup_date__gte=epochToDate(request.data["pickup_date"])) & 
                   Q(return_date__lte=epochToDate(request.data["return_date"]))) &
                   Q(is_active=True)
                   ).values_list("car") 
        # all cars in given location
        cars_not_in_location= models.Car.objects.exclude(
                    location=request.data["pickup_location"]
                    ).values_list("id") 
        car_different_city = list(chain(cars_busy, cars_not_in_location))
        # merge all unaviable cars
        unavailable_cars = ()
        for t in car_different_city:
            unavailable_cars += t  
        # serialize aviable cars
        print(unavailable_cars)
        cars = models.Car.objects.exclude(Q(id__in=unavailable_cars) | Q(is_allocated=True))  
        serializer = serializers.CarSerializer(cars, many=True, context={"request": request})
        return Response(serializer.data)

"""
example request
{
    "user": 7,  
    "car": 1, 
    "pickup_location": 1, 
    "return_location": 1, 
    "pickup_date": 1653696000,
    "return_date": 1654128000
}
"""
@api_view(['POST', 'GET', 'DELETE'])
# @permission_classes([IsAuthenticated])
def reservation(request, id = None):
    print("id is", id)
    if request.method == "GET":
        # reservations = models.Reservation.objects.filter(user_id=request.user.id)
        # TODO: delete line below
        reservations = models.Reservation.objects.filter(user_id=7)
        serializer = serializers.ReservationSerializer(reservations, many=True, context={"request": request})
        return Response(serializer.data)
    elif request.method == "POST":
        serializer_data = request.data 
        request.data["user"] = models.User.objects.filter(id=request.data["user"])[0]
        request.data["car"] = models.Car.objects.filter(id=request.data["car"])[0]
        request.data["pickup_location"] = models.Location.objects.filter(id=request.data["pickup_location"])[0]
        request.data["return_location"] = models.Location.objects.filter(id=request.data["return_location"])[0]
        request.data["pickup_date"] = epochToDate(request.data["pickup_date"])
        request.data["return_date"] = epochToDate(request.data["return_date"])

        # save reservation 
        serializer = serializers.ReservationSerializer(data=request.data)
        serializer.is_valid() # fix this: why data invalid 
        serializer.create(serializer.data)
        return Response("Reservation created")
    elif request.method == "DELETE":
        # deactivate reservation
        if id:
            reservation = models.Reservation.objects.filter(id=id)[0]
            reservation.is_active = False 
            reservation.save()
            return Response("reservation " + id + " is deactivated")
        return Response( id, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def allocate_car(request, id):
    car = models.Car.objects.get(pk=id)
    car.is_allocated = True
    car.save()
    allocate_second = 300
    t = Timer(allocate_second, deallocate_car, [id])
    t.start()
    return Response("car {} will be deallocated in {} second".format(id, allocate_second))


