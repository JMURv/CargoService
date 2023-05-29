from django.core.validators import MaxValueValidator
from django.db import models

from api.validators import unique_number_validator


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"City: {self.city}"


class Car(models.Model):
    unique_number = models.CharField(max_length=5, unique=True, validators=[unique_number_validator])
    current_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    carrying_capacity = models.IntegerField(
        validators=[
            MaxValueValidator(1000)
        ])

    def __str__(self):
        return f"Car: {self.unique_number}"


class Shipment(models.Model):
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickups')
    delivery_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='deliveries')
    weight = models.IntegerField()
    description = models.TextField()
