from rest_framework.serializers import ModelSerializer
import base.models as models 

class UserSerializer(ModelSerializer):
    class Meta: 
        model = models.User
        fields = "__all__"
