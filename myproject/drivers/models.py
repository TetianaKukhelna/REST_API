from django.db import models


class Driver(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name="id"
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "driver"

    def __repr__(self):
        return f"<Driver #{self.id}> first_name={self.first_name} last_name={self.last_name}"


class Vehicle(models.Model):
    id = models.BigAutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name="id"
    )
    driver = models.ForeignKey(
        null=True, on_delete=models.deletion.CASCADE, to="drivers.Driver", db_column="driver_id"
    )
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    plate_number = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "vehicle"

    def __repr__(self):
        return f"<Vehicle #{self.id}> make={self.make} model={self.model}"
