from rest_framework.serializers import ModelSerializer
import base.models as models 


class UserSerializer(ModelSerializer):
    class Meta: 
        model = models.User
        fields = ["first_name", "last_name", "email", "password"]

class CustomerSerializer(ModelSerializer):
    class Meta: 
        model = models.Customer
        fields = "__all__"
