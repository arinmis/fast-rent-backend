import datetime
import base.models as models

def epochToDate(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')

def deallocate_car(car):
    print("deallocate_car")
