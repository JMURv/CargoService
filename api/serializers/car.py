from rest_framework import serializers
from api.models import Car


class CarUpdateSerializer(serializers.ModelSerializer):
    current_location = serializers.CharField()
    unique_number = serializers.CharField(read_only=True)
    carrying_capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = [
            'unique_number',
            'current_location',
            'carrying_capacity',
        ]


class CarSerializer(serializers.ModelSerializer):
    current_location = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Car
        fields = [
            'id',
            'unique_number',
            'current_location',
            'carrying_capacity',
        ]
