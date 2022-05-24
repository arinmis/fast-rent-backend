from rest_framework.serializers import ModelSerializer, SlugRelatedField
import base.models as models 


class UserSerializer(ModelSerializer):
    class Meta: 
        model = models.User
        fields = ["first_name", "last_name", "email", "password"]

class CustomerSerializer(ModelSerializer):
    user = UserSerializer() 

    class Meta: 
        model = models.Customer
        fields = ["citizen_id", "user"] 
