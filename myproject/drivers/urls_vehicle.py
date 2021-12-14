from django.urls import path

from . import views_vehicle


# MVC
urlpatterns = [
    path("vehicle/", views_vehicle.create_vehicle),
    path("vehicle/<int:vehicle_id>/", views_vehicle.vehicle),
    path("set_driver/<int:vehicle_id>/", views_vehicle.set_or_unset_driver),
]
