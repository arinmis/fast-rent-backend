from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from . import utils
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
                (Q(pickup_date__gte=utils.epoch_to_date(request.data["pickup_date"])) &
                    Q(return_date__lte=utils.epoch_to_date(request.data["return_date"]))) &
                Q(is_active=True)
                ).values_list("car")
        print("cars busy", cars_busy)
        # all cars in given location
        cars_not_in_location= models.Car.objects.exclude(
                location=request.data["pickup_location"]
                ).values_list("id")
        print("cars_not_in_location", cars_not_in_location)
        # cars not allocated
        cars_allocated = models.Car.objects.filter(Q(allocated_by__isnull=False)).values_list("id")
        print("cars_allocated", cars_allocated)
        car_different_city = list(chain(cars_busy, cars_not_in_location, cars_allocated))
        # merge all unaviable cars
        unavailable_cars = ()
        for t in car_different_city:
            unavailable_cars += t
        # serialize aviable cars
        print("un available car: ", unavailable_cars)
        # Q(id__in=unavailable_cars) |
        cars = models.Car.objects.exclude(id__in=unavailable_cars)
        serializer = serializers.CarSerializer(cars, many=True, context={"request": request})
        return Response(serializer.data)


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def car_crud(request, id = None):
    if request.method == "POST":
        try:
            car = models.Car.objects.create(
                    brand_type = models.BrandType.objects.get(pk=request.data["brand_type"]),
                    fuel_type = models.FuelType.objects.get(pk=request.data["fuel_type"]),
                    transmission_type =models.TransmissionType.objects.get(pk=request.data["transmission_type"]),
                    location = models.Location.objects.get(pk=request.data["location"]),
                    photo = request.data["photo"],
                    daily_price = request.data["daily_price"],
                    )
            print("daily_price", request.data["daily_price"])
            car.save()
            serializer = serializers.CarSerializer(car, context={"request": request})
            print(car)
            print(serializer.data)
            return Response(serializer.data)
        except:
            return Response("post a valid car", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if id == None:
            return Response("car id is needed", status=status.HTTP_400_BAD_REQUEST)
        car = models.Car.objects.get(pk=id)
        car.delete()
        return Response("car {} is has been deleted".format(id))


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
@permission_classes([IsAuthenticated])
def reservation(request, id = None):
    print("id is", id)
    if request.method == "GET":
        reservations = models.Reservation.objects.filter(user_id=request.user.id, pickup_date__gte=datetime.datetime.now(), is_active=True)
        serializer = serializers.ReservationSerializer(reservations, many=True, context={"request": request})
        print(request.user.id, serializer.data)
        return Response(serializer.data)
    elif request.method == "POST":
        # try:
        print("reservation being is creating", request.data, "data")
        print(type(models.Car.objects.get(id=request.data["car"])))

        user = models.User.objects.get(id=request.data["user"])
        car = models.Car.objects.get(id=request.data["car"])

        # check whether the use has allocated car before reservations
        if car.is_reserved or (car.allocated_by != None and user.id != car.allocated_by.id):
            print(car.is_reserved)
            print(car.allocated_by)
            print(user.id, car.allocated_by.id)
            return Response(
                     "car {} doesn't available right now, select another one".format(id),
                     status=status.HTTP_406_NOT_ACCEPTABLE)

        reservation = models.Reservation.objects.create(
                user = user,  
                car = car,  
                pickup_location = models.Location.objects.get(id=request.data["pickup_location"]),
                return_location = models.Location.objects.get(id=request.data["return_location"]),
                pickup_date = utils.epoch_to_date(request.data["pickup_date"]),
                return_date = utils.epoch_to_date(request.data["return_date"]),
                is_active=True,
                )
        reservation.save()

        # mark car as reserved 
        car.is_reserved = True
        car.save()
        return Response("Reservation created")
        """
        except Exception as e:
            print("here", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        """
        
    elif request.method == "DELETE":
        # deactivate reservation
        if id:
            reservation = models.Reservation.objects.filter(id=id)[0]
            reservation.car.is_reserved = False 
            reservation.car.allocated_by = None 
            reservation.is_active = False
            # save changes
            reservation.save()
            reservation.car.save()
            print("car reservatsion:", reservation.car.is_reserved)
            return Response("reservation " + id + " is deactivated")
        return Response(id, status=status.HTTP_400_BAD_REQUEST)


"""
reservations which's pick-up
date passed are called rent
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rent(request):
    reservations = models.Reservation.objects.filter(Q(user_id=request.user.id) & (Q(pickup_date__lte=datetime.datetime.now()) | Q(is_active=False)))
    serializer = serializers.ReservationSerializer(reservations, many=True, context={"request": request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allocate_car(request, id):
    car = models.Car.objects.get(pk=id)
    # if already allocated return error
    print("is car allocated: ", car.allocated_by)
    if (car.allocated_by != None):
        return Response("car {} already has been allocated".format(id), status=status.HTTP_406_NOT_ACCEPTABLE)
    car.allocated_by = request.user
    car.save()
    # time for allocation
    allocate_second = 10
    t = Timer(allocate_second, utils.deallocate_car, [id])
    print("car {} will be deallocated in {} sn".format(id, allocate_second))
    t.start()
    return Response({"deallocate_time": str(allocate_second)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deallocate_car(request, id):
    utils.deallocate_car(id)
    return Response("car {} is deallocated".format(id))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def statistics(request):
    response = {}
    response["reserved_cars"] =  len(models.Car.objects.filter(is_reserved=True))
    response["not_reserved_cars"] =  len(models.Car.objects.filter(is_reserved=False))
    response["reservations_active"] = len(models.Reservation.objects.filter(is_active=True))
    response["reservations_passive"] = len(models.Reservation.objects.filter(is_active=False))
    return Response(response)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_reservations(request):
    print("here")
    if request.method == "GET":
        reservations = models.Reservation.objects.filter(is_active=True)
        serializer = serializers.ReservationSerializer(reservations, many=True, context={"request": request})
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_rents(request):
    print("here")
    if request.method == "GET":
        reservations = models.Reservation.objects.all()
        serializer = serializers.ReservationSerializer(reservations, many=True, context={"request": request})
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customers(request):
    print("here")
    user  = models.User.objects.filter(is_staff=False)
    serializer = serializers.UserSerializer(user, many=True, context={"request": request})
    return Response(serializer.data)


