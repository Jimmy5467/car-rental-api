import os
# from car_rental.car_rental.settings import AUTH_USER_MODEL as User
from accounts.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.Car.id, ext)
    return os.path.join(filename)


# Create your models here.
class Car(models.Model):
    ownerId = models.ForeignKey(User, on_delete=models.CASCADE)  # ownerId = models.IntegerField()
    company = models.CharField(max_length=128)
    car_model_name = models.CharField(max_length=128, null=False, blank=False)
    seats = models.IntegerField(default=4, validators=[MaxValueValidator(10), MinValueValidator(1)])
    car_type = models.CharField(max_length=128)
    fuel = models.CharField(max_length=16)
    rent = models.FloatField(default=4.5)
    number_plate = models.CharField(max_length=16, unique=True, error_messages={'unique': 'Car exist in database already.'})
    issue = models.TextField(max_length=256, error_messages={'max_length': 'message length must be less then 250'},
                             null=True, blank=True)
    city = models.CharField(max_length=64)
    pickup_address = models.TextField()
    drop_address = models.TextField()
    is_verified = models.BooleanField(null=True, blank=True)
    available_from = models.DateTimeField()
    availability_ends = models.DateTimeField()
    rc_number = models.CharField(max_length=16,)
    AC = models.BooleanField()
    AorM = models.BooleanField()
    front_image = models.ImageField(null=True, blank=True, upload_to=content_file_name)
    back_image = models.ImageField(null=True, blank=True, upload_to=content_file_name)

    def __str__(self):
        return self.number_plate


class Booked(models.Model):
    carId = models.ForeignKey(Car, on_delete=models.CASCADE)  # carId = models.IntegerField()
    car_model_name = models.CharField(max_length=128, null=True, blank=True)
    # car_model_name = models.CharField(max_length=128, null=True, blank=True)
    ownerId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='s_ownerId')
    renterId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='s_renterId')
    payable_amount = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    payment_status = models.BooleanField(default=False, null=True, blank=True)
    owner_phone = models.CharField(max_length=10)
    renter_phone = models.CharField(max_length=10)
    booked_on = models.DateTimeField(auto_now_add=True)

    # journey_status = models.BooleanField()

    def __str__(self):
        return self.car_model_name


class Feedback(models.Model):
    carId = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], null=False, blank=False)
    feedback = models.TextField(max_length=30, blank=False, null=False)


class Cancel(models.Model):
    renterId = models.ForeignKey(User, on_delete=models.CASCADE)
    cancelled_on = models.DateTimeField(null=False, blank=False)
    carId = models.ForeignKey(Car, on_delete=models.CASCADE)
