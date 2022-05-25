from rest_framework.serializers import ModelSerializer, SlugRelatedField
import base.models as models 


class UserSerializer(ModelSerializer):
    class Meta: 
        model = models.User
        fields = ["username", "first_name", "last_name", "email", "password"]

    # create new user
    def create(self, validated_data):
        user = models.User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    # update existing user
    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.save()


class CustomerSerializer(ModelSerializer):
    user = UserSerializer() 

    class Meta: 
        model = models.Customer
        fields = ["citizen_id", "user"] 

    # create new 
    def create(self, validated_data):
        user_serializer = UserSerializer(data=validated_data.get("user")) 
        # print(user_serializer.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            customer = models.Customer.objects.create(
                    user=user, 
                    citizen_id = validated_data.get("citizen_id")
                    )
            print("here is user", user.username, user.first_name, user.last_name)
            return customer 

    def update(self, instance, validated_data):
        print("helloooo: ", instance)
        user_serializer = UserSerializer(data=validated_data.get("user")) 
        # update citizen_id
        customer = models.Customer.object.filter(id)
        if user_serializer.is_valid():
            print("hererererer")
            user_serializer.update(user_serializer.data)


"""
{
    "citizen_id": "101010101010",
    "user": {
        "username": "temp",
        "first_name": "temp",
        "last_name": "temp",
        "email": "temp@example.com",
        "password": "temp1234"
    }
}
"""
