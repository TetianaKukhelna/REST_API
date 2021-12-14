from django.urls import path

from . import views_driver


# MVC GET driver/lalala
urlpatterns = [
    path("driver/", views_driver.create_driver),
    path("driver/<int:pk>/", views_driver.driver),
]
