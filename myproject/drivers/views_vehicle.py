import logging

from django.db.models import Exists, OuterRef
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from .models import Driver, Vehicle
from .serializers import VehicleSerializer
from .utils import is_valid_yes_no, VALID_YES


@api_view(["GET", "PATCH", "DELETE"])
def vehicle(request, vehicle_id):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        vehicle = Vehicle.objects.get(pk=vehicle_id)
    except Vehicle.DoesNotExist:
        return JsonResponse(
            {"message": "The vehicle does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        logging.info(f"GET vehicle #{vehicle_id}")
        veh_serializer = VehicleSerializer(vehicle)
        return JsonResponse(veh_serializer.data)

    elif request.method == "PATCH":
        veh_data = JSONParser().parse(request)
        veh_data.pop("driver_id", None)
        veh_serializer = VehicleSerializer(vehicle, data=veh_data)
        if veh_serializer.is_valid():
            veh_serializer.save()
            return JsonResponse(veh_serializer.data)
        return JsonResponse(veh_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        vehicle.delete()
        return JsonResponse(
            {"message": "Vehicle was deleted successfully!"}, status=status.HTTP_204_NO_CONTENT
        )


@api_view(["GET", "POST"])
def create_vehicle(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == "POST":
        vehicle_data = JSONParser().parse(request)
        vehicle_ser = VehicleSerializer(data=vehicle_data)
        if vehicle_ser.is_valid():
            vehicle_ser.save()
            return JsonResponse(vehicle_ser.data, status=status.HTTP_201_CREATED)
        return JsonResponse(vehicle_ser.errors, status=status.HTTP_400_BAD_REQUEST)

    with_drivers = request.query_params.get("with_driver")
    if with_drivers:
        with_drivers = with_drivers.lower()

    if with_drivers and not is_valid_yes_no(with_drivers):
        return JsonResponse(
            "Invalid with_driver format must by yes/no", status=status.HTTP_404_NOT_FOUND
        )

    if with_drivers and with_drivers == VALID_YES:
        vehicle = Vehicle.objects.filter(driver_id__isnull=False).all()  # TODO: add limit offset
    elif with_drivers:
        vehicle = (
            Vehicle.objects.filter(driver_id__isnull=True)
            .values_list(
                "id", "make", "model", "plate_number", "created_at", "updated_at", named=True
            )
            .all()
        )
    else:
        vehicle = Vehicle.objects.all()

    vehicle_serializer = VehicleSerializer(vehicle, many=True)
    return JsonResponse(vehicle_serializer.data, safe=False)


@api_view(["POST"])
def set_or_unset_driver(request, vehicle_id):
    """
    Set or unset driver
    """
    if request.method != "POST":
        return JsonResponse({"message": "Page not Found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        vehicle = Vehicle.objects.get(pk=vehicle_id)
    except Vehicle.DoesNotExist:
        return JsonResponse(
            {"message": "The vehicle does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if vehicle.driver_id:
        vehicle.driver_id = None
        vehicle.save()
        return JsonResponse(VehicleSerializer(vehicle).data, status=status.HTTP_200_OK)

    # select * from driver d
    # where not exists(
    #     select driver_id
    #     from vehicle v
    #     where v.driver_id == d.id
    # );
    driver = Driver.objects.filter(
        ~Exists(Vehicle.objects.filter(driver_id=OuterRef("pk")))
    ).first()

    if not driver:
        return JsonResponse(
            {"message": "There is not available driver now, try after 5 min"},
            status=status.HTTP_404_NOT_FOUND,
        )

    vehicle.driver_id = driver.id
    vehicle.save()
    return JsonResponse(VehicleSerializer(vehicle).data, status=status.HTTP_200_OK)
