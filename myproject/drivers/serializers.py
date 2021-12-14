import datetime

from rest_framework import serializers

from .models import Driver, Vehicle
from .utils import DATETIME_FORMAT

PLATE_FIELD_REG = '^\w\w \d\d\d\d \w\w'


class DriverSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True, max_length=20)
    last_name = serializers.CharField(required=True, max_length=20)
    created_at = serializers.DateTimeField(
        required=False, format=DATETIME_FORMAT, default=datetime.datetime.utcnow()
    )
    updated_at = serializers.DateTimeField(
        required=False, format=DATETIME_FORMAT, default=datetime.datetime.utcnow()
    )

    def to_representation(self, instance):
        resp = {
            "id": instance.id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "created_at": instance.created_at.strftime(DATETIME_FORMAT),
        }
        if instance.updated_at:
            resp["updated_at"] = instance.updated_at.strftime(DATETIME_FORMAT)
        return resp

    def create(self, validated_data):
        """
        Create and return a new `Driver` instance, given the validated data.
        """
        validated_data.pop("updated_at", None)
        return Driver.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Driver` instance, given the validated data.
        """
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.updated_at = datetime.datetime.utcnow()
        instance.save()
        return instance

    class Meta:
        model = Driver
        fields = ("id", "first_name", "last_name", "created_at", "updated_at")


class VehicleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=False)
    make = serializers.CharField(required=False, max_length=20)
    model = serializers.CharField(required=False, max_length=20)
    plate_number = serializers.RegexField(PLATE_FIELD_REG, required=False, max_length=20)
    created_at = serializers.DateTimeField(
        required=False, format=DATETIME_FORMAT, default=datetime.datetime.utcnow()
    )
    updated_at = serializers.DateTimeField(
        required=False, format=DATETIME_FORMAT, default=datetime.datetime.utcnow()
    )

    driver = serializers.RelatedField(read_only=True)

    def to_representation(self, instance):
        resp = {}
        if getattr(instance, "id", None):
            resp["id"] = instance.id
        if getattr(instance, "make", None):
            resp["make"] = instance.make
        if getattr(instance, "model", None):
            resp["model"] = instance.model
        if getattr(instance, "plate_number", None):
            resp["plate_number"] = instance.plate_number
        if getattr(instance, "created_at", None):
            resp["created_at"] = instance.created_at.strftime(DATETIME_FORMAT)
        if getattr(instance, "updated_at", None):
            resp["updated_at"] = instance.updated_at.strftime(DATETIME_FORMAT)
        if getattr(instance, "driver", None):
            resp["driver"] = DriverSerializer(instance.driver).to_representation(instance.driver)
        return resp

    def create(self, validated_data):
        """
        Create and return a new `Driver` instance, given the validated data.
        """
        validated_data.pop("updated_at", None)
        return Vehicle.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Vehicle` instance, given the validated data.
        """
        instance.make = validated_data.get("make", instance.make)
        instance.model = validated_data.get("model", instance.model)
        instance.plate_number = validated_data.get("plate_number", instance.plate_number)
        instance.driver_id = validated_data.get("driver_id", instance.driver_id)
        instance.updated_at = datetime.datetime.utcnow()
        instance.save()
        return instance

    class Meta:
        model = Vehicle
        fields = ("id", "make", "model", "plate_number", "created_at", "updated_at", "driver")
