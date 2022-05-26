from django.http import JsonResponse 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from . import serializers
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def car(request):
    print("here")
    cars = models.Car.objects.all()
    print("cars: ", cars[0].daily_price)
    serializer = serializers.CarSerializer(cars, many=True, context={"request": request})
    return Response(serializer.data)

