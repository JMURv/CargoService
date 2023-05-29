import random
from celery import shared_task
from api.models import Car, Location


@shared_task
def update_car_locations():
    cars = Car.objects.all()
    for car in cars:
        location = random.choice(Location.objects.all())
        car.current_location = location
        car.save()
