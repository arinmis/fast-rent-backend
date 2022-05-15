from django.http import JsonResponse 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getHello(request):
    return Response("restricted hello")


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user(request, id):
    if request.method == 'GET':
        user  = models.User.objects.filter(id=id) 
        serializer = serializers.UserSerializer(user, many=True)
        return Response(serializer.data)
    elif requested.method == "PUT":
        pass
    return Response("signup")
