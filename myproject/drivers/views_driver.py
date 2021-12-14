import logging

from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from .models import Driver

from .serializers import DriverSerializer
from .utils import convert_format, is_valid_date


@api_view(["GET", "PATCH", "DELETE"])
def driver(request, pk):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        driver = Driver.objects.get(pk=pk)
    except Driver.DoesNotExist:
        return JsonResponse(
            {"message": "The driver does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        logging.info(f"GET driver #{pk}")
        tutorial_serializer = DriverSerializer(driver)
        return JsonResponse(tutorial_serializer.data)

    elif request.method == "PATCH":
        driver_data = JSONParser().parse(request)
        driver_serializer = DriverSerializer(driver, data=driver_data)
        if driver_serializer.is_valid():
            driver_serializer.save()
            return JsonResponse(driver_serializer.data)
        return JsonResponse(driver_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        driver.delete()
        return JsonResponse(
            {"message": "Driver was deleted successfully!"}, status=status.HTTP_204_NO_CONTENT
        )


@api_view(["GET", "POST"])
def create_driver(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == "POST":
        driver_data = JSONParser().parse(request)
        driver_ser = DriverSerializer(data=driver_data)
        if driver_ser.is_valid():
            driver_ser.save()
            return JsonResponse(driver_ser.data, status=status.HTTP_201_CREATED)
        return JsonResponse(driver_ser.errors, status=status.HTTP_400_BAD_REQUEST)

    params_gte = request.query_params.get("created_at__gte")
    params_lte = request.query_params.get("created_at__lte")
    if params_gte and is_valid_date(params_gte):
        driver = Driver.objects.filter(
            created_at__gte=convert_format(params_gte)
        ).all()  # TODO: add limit offset
    elif params_lte and is_valid_date(params_lte):
        driver = Driver.objects.filter(
            created_at__lte=convert_format(params_lte)
        ).all()  # TODO: add limit offset
    elif params_gte or params_lte:
        return JsonResponse({"error": "Invalid datetime format"}, status=status.HTTP_404_NOT_FOUND)
    else:
        driver = Driver.objects.all()

    driver_serializer = DriverSerializer(driver, many=True)
    return JsonResponse(driver_serializer.data, safe=False)
