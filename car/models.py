import os
# from car_rental.car_rental.settings import AUTH_USER_MODEL as User
from accounts.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from uuid import uuid4
from django.utils import timezone
from django.utils.deconstruct import deconstructible


#
# now = timezone.now()

@deconstructible
class content_file_name(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

# def wrapper(instance, filename):
#     ext = filename.split('.')[-1]
#     # get filename
#     if instance.pk:
#         filename = '{}.{}'.format(instance.pk, ext)
#     else:
#         # set filename as random string
#         filename = '{}.{}'.format(uuid4().hex, ext)
#     # return the whole path to the file
#     return os.path.join(path, filename)
# return wrapper

# def content_file_name(instance, filename):
#     ext = filename.split('.')[-1]
#     filename = "%s.%s" % (instance.car.id, ext)
#     return os.path.join(filename)


# Create your models here.
class Car(models.Model):
    ownerId = models.ForeignKey(User, on_delete=models.CASCADE)  # ownerId = models.IntegerField()
    company = models.CharField(max_length=128, null=True, blank=True)
    car_model_name = models.CharField(max_length=128, null=True, blank=True)
    seats = models.IntegerField(default=4, validators=[MaxValueValidator(10), MinValueValidator(1)])
    car_type = models.CharField(max_length=128, null=True, blank=True)
    fuel = models.CharField(max_length=16, null=True, blank=True)
    rent = models.FloatField(null=True, blank=True)
    number_plate = models.CharField(max_length=16, unique=True,
                                    error_messages={'unique': 'Car exist in database already.'})
    issue = models.TextField(max_length=256, error_messages={'max_length': 'message length must be less then 250'},
                             null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    pickup_address = models.TextField(null=True, blank=True)
    drop_address = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(null=True, blank=True)
    available_from = models.DateField()
    availability_ends = models.DateField()
    # rc_number = models.CharField(max_length=16, null=True, blank=True) ##
    AC = models.BooleanField()
    AorM = models.BooleanField()
    front_image = models.ImageField(null=True, blank=True, upload_to=content_file_name('car_front/'))
    back_image = models.ImageField(null=True, blank=True, upload_to=content_file_name('car_back/'))
    buying_year = models.IntegerField(default=2021)
    mileage = models.FloatField(default=24)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.number_plate


class Booked(models.Model):
    carId = models.ForeignKey(Car, on_delete=models.CASCADE)  # carId = models.IntegerField()
    company = models.CharField(max_length=128, null=True, blank=True)
    car_model_name = models.CharField(max_length=128, null=True, blank=True)
    ownerId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='s_ownerId')
    renterId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='s_renterId')
    payable_amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    booked_on = models.DateField()  ###
    # payment_status = models.BooleanField(default=False, null=True, blank=True) ##
    address = models.TextField(null=True, blank=True)
    owner_phone = models.CharField(max_length=10, default=None) ##
    renter_phone = models.CharField(max_length=10, default=None)##

    # journey_status = models.BooleanField()


class Feedback(models.Model):
    carId = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], null=True, blank=True)
    feedback = models.TextField(max_length=30, blank=True, null=True)


class Cancel(models.Model):  # full on backend side
    renterId = models.ForeignKey(User, on_delete=models.CASCADE)
    cancelled_on = models.DateField()
    # bookId = models.ForeignKey(Booked, on_delete=models.CASCADE, default=1)
    # # # # # # #
