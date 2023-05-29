import random
from django.shortcuts import get_object_or_404
from api.models import Location, Car
from api.serializers.car import CarSerializer, CarUpdateSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response


class ListCreateCarView(ListCreateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    def post(self, request, *args, **kwargs):
        unique_number = request.data.get('unique_number')
        carrying_capacity = request.data.get('carrying_capacity')
        location = random.choice(Location.objects.all())
        truck = Car.objects.create(
            unique_number=unique_number,
            current_location=location,
            carrying_capacity=carrying_capacity
        )

        serializer = CarSerializer(truck)
        return Response(serializer.data)


class UpdateCarView(RetrieveUpdateDestroyAPIView):
    serializer_class = CarUpdateSerializer

    def patch(self, request, *args, **kwargs):
        car = self.get_object()
        location_zip_code = request.data.get('current_location')
        location = get_object_or_404(Location, zip_code=location_zip_code)
        car.current_location = location
        car.save()
        serializer = CarUpdateSerializer(car)
        return Response(serializer.data)

    def get_object(self):
        return get_object_or_404(Car, id=self.kwargs.get('car_id'))
