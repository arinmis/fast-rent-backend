import datetime
import base.models as models

def epoch_to_date(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')

# deacllocate car with given id 
def deallocate_car(id):
    car = models.Car.objects.get(pk=id)
    car.allocated_by = None 
    car.save()
    print("car {} is deallocated" .format(car.id))
