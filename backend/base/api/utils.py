import datetime
import base.models as models

def epochToDate(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')

# deacllocate car with given id 
def deallocate_car(id):
    car = models.Car.objects.get(pk=id)
    car.is_allocated = False
    car.save()
    print("car.is_allocated", id, car.is_allocated)
