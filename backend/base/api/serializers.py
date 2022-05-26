from rest_framework.serializers import ModelSerializer, SlugRelatedField, SerializerMethodField
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
        print("here: ", instance.password)
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        try:
            instance.set_password(validated_data['password'])
        except:
            print("No password to update")

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
        # update citizen id
        instance.citizen_id = validated_data.get("citizen_id")
        instance.save()
        # save user info
        user_serializer = UserSerializer(data=validated_data.get("user"))
        # update citizen_id
        if user_serializer.is_valid() or True: # skip validation
            user = models.User.objects.filter(id=instance.user_id)[0]
            user_serializer.update(user, user_serializer.data)


class LocationSerializer(ModelSerializer):
    class Meta:
        model = models.Location
        fields = "__all__"



class TransmissionTypeSerializer(ModelSerializer):
    class Meta:
        model = models.TransmissionType
        fields = ["transmission_type"]

class FuelTypeSerializer(ModelSerializer):
    class Meta:
        model = models.FuelType
        fields = ["fuel_type"]

class BrandTypeSerializer(ModelSerializer):
    class Meta:
        model = models.BrandType
        fields = ["brand_type"]

class CarSerializer(ModelSerializer):
    photo_url = SerializerMethodField()
    transmission_type = TransmissionTypeSerializer(many=False)
    brand_type = BrandTypeSerializer(many=False)
    fuel_type = FuelTypeSerializer(many=False)

    class Meta:
        model = models.Car
        fields = "__all__"

    def get_photo_url(self, car):
        request = self.context.get('request')
        photo_url = car.photo.url
        return request.build_absolute_uri(photo_url)


class ReservationSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Reservation
        fields = "__all__" 

    def create(self, validated_data):
        reservation = models.Reservation.objects.create(
            pickup_date = validated_data["pickup_date"],
            return_date = validated_data["return_date"],
            user = validated_data["user"],
            car = validated_data["car"],
            pickup_location = validated_data["pickup_location"],
            return_location = validated_data["return_location"],
        )



