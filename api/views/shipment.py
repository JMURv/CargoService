from geopy.distance import geodesic
from django.shortcuts import get_object_or_404
from api.models import Location, Car, Shipment
from api.serializers.shipment import ShipmentSerializer, ShipmentUpdateSerializer

from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response


class FilterShipmentsView(APIView):
    def get(self, request):
        weight = request.query_params.get('weight')
        distance = request.query_params.get('distance')
        shipments = Shipment.objects.filter(weight=weight)

        if distance:
            filtered_shipments = []
            for shipment in shipments:
                nearest_trucks = []
                for truck in Car.objects.all():
                    truck_distance = geodesic(
                        (shipment.pickup_location.latitude, shipment.pickup_location.longitude),
                        (truck.current_location.latitude, truck.current_location.longitude)
                    ).miles

                    if truck_distance <= float(distance):
                        nearest_trucks.append({
                            'truck': truck.unique_number,
                            'distance': truck_distance
                        })

                if nearest_trucks:
                    filtered_shipments.append({
                        'shipment': ShipmentSerializer(shipment).data,
                        'nearest_trucks': nearest_trucks
                    })
            return Response(filtered_shipments)

        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)


class ListCreateShipmentsView(ListCreateAPIView):
    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()

    def post(self, request, *args, **kwargs):
        pickup_zip_code = request.data.get('pickup_location')
        delivery_zip_code = request.data.get('delivery_location')
        weight = request.data.get('weight')
        description = request.data.get('description')

        pickup_location = get_object_or_404(Location, zip_code=pickup_zip_code)
        delivery_location = get_object_or_404(Location, zip_code=delivery_zip_code)

        shipment = Shipment.objects.create(
            pickup_location=pickup_location,
            delivery_location=delivery_location,
            weight=weight,
            description=description
        )

        shipment_data = ShipmentSerializer(shipment).data
        return Response({'shipment': shipment_data})


class GetUpdateDeleteShipmentView(RetrieveUpdateDestroyAPIView):
    serializer_class = ShipmentSerializer
    update_serializer = ShipmentUpdateSerializer

    def get(self, request, *args, **kwargs):
        shipment = get_object_or_404(Shipment, id=kwargs.get('shipment_id'))
        cars = Car.objects.all()
        nearest_cars = []
        for car in cars:
            distance = geodesic(
                (shipment.pickup_location.latitude, shipment.pickup_location.longitude),
                (car.current_location.latitude, car.current_location.longitude)
            ).miles
            car_data = {
                'number': car.unique_number,
                'distance': distance
            }
            nearest_cars.append(car_data)
        shipment_data = self.serializer_class(shipment).data
        shipment_data['nearest_cars'] = nearest_cars
        return Response(shipment_data)

    def patch(self, request, *args, **kwargs):
        shipment = get_object_or_404(Shipment, id=kwargs.get('shipment_id'))
        serializer = self.update_serializer(shipment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        shipment = get_object_or_404(Shipment, id=kwargs.get('shipment_id'))
        shipment.delete()
        return Response({'message': 'Shipment deleted successfully.'})