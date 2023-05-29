from geopy.distance import geodesic
from rest_framework import serializers
from api.models import Shipment, Car


class ShipmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['weight', 'description']


class ShipmentSerializer(serializers.ModelSerializer):
    pickup_location = serializers.CharField()
    delivery_location = serializers.CharField()
    nearest_cars = serializers.SerializerMethodField()

    def get_nearest_cars(self, obj):
        cars = Car.objects.all()
        nearest_cars = 0
        for car in cars:
            distance = geodesic(
                (obj.pickup_location.latitude, obj.pickup_location.longitude),
                (car.current_location.latitude, car.current_location.longitude)
            ).miles
            if distance <= 450:
                nearest_cars += 1
        return nearest_cars

    class Meta:
        model = Shipment
        fields = [
            'id',
            'pickup_location',
            'delivery_location',
            'nearest_cars',
            'weight',
            'description',
        ]
