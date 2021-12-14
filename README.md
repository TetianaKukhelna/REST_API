# Yalantis test project for PythonSchool 14.12.2021

### This application is manage system for Driver and their Vehicles

We use last `Python 3.9.9`, `Django` and `SQLite` for it.

Project wrap in Docker and all interfaces you can see in `Makefile`

To run project just call `make up` and Docker pull project and run it

Project have some endpoints for driver:
1. GET http://0.0.0.0:3889/drivers/driver/<driver_id>/
2. GET http://0.0.0.0:3889/drivers/driver/
3. GET http://0.0.0.0:3889/drivers/driver/?created_at__gte=10-11-2021
4. GET http://0.0.0.0:3889/drivers/driver/?created_at__lte=10-11-2021
5. POST http://0.0.0.0:3889/drivers/driver/
6. PATCH http://0.0.0.0:3889/drivers/driver/<driver_id>/
7. DELETE http://0.0.0.0:3889/drivers/driver/<driver_id>/


And for vehicles:
1. GET http://0.0.0.0:3889/vehicles/vehicle/<vehicle_id>/
2. POST http://0.0.0.0:3889/vehicles/vehicle/
3. PATCH http://0.0.0.0:3889/vehicles/vehicle/<vehicle_id>/
4. DELETE http://0.0.0.0:3889/vehicles/vehicle/<vehicle_id>/
5. GET http://0.0.0.0:3889/vehicles/vehicle/
6. GET http://0.0.0.0:3889/vehicles/vehicle/?with_drivers=yes
7. GET http://0.0.0.0:3889/vehicles/vehicle/?with_drivers=no
8. POST http://0.0.0.0:3889/vehicles/set_driver/<vehicle_id>/


Have fun