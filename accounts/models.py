from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from django.utils.deconstruct import deconstructible
import os


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


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

#
# def content_file_name(instance, filename):
#     ext = filename.split('.')[-1]
#     filename = "/profile/" + "%s.%s" % (instance.User.id, ext)
#     return os.path.join(filename)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=250, unique=True,
                                error_messages={"unique": "The username you enetered is not unique."})
    email = models.EmailField(max_length=250, unique=True,
                              error_messages={"unique": "The email you enetered is not unique."})
    phone = models.CharField(max_length=10, null=True, blank=True)  # , unique=True
    # first_name = models.CharField(max_length=30, blank=True, null=True)  ##
    # last_name = models.CharField(max_length=30, blank=True, null=True)  ##
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    receive_newsletter = models.BooleanField(default=False)
    city = models.CharField(max_length=30, blank=True, null=True)
    license = models.CharField(max_length=15, blank=True, null=True)
    # time in just day format
    # username = models.CharField(_('password'), max_length=128, unique=True)
    # email = models.EmailField(_('email address'), max_length=128, unique=True)
    # phone = models.IntegerField(_('phone'))
    # first_name = models.CharField(_('first name'), max_length=50, blank=True, null=True)
    # last_name = models.CharField(_('last name'),  max_length=50, blank=True, null=True)
    # is_active = models.BooleanField(_('active'), default=True)
    # is_staff = models.BooleanField(_('staff'), default=False)
    # is_superuser = models.BooleanField(_('superuser'), default=False)
    # date_joined = models.DateTimeField(_('Joined on'), default=timezone.now)
    # receive_newsletter = models.BooleanField(_('newsletter'), default=False)
    # city = models.CharField(_('city'), max_length=100, blank=True, null=True)
    # license = models.CharField(_('license'), max_length=15)
    #
    #
    # about_me = models.TextField(max_length=500, blank=True, null=True)
    # profile_image = models.ImageField(null=True)
    # birth_date = models.DateTimeField(blank=True, null=True)
    # address = models.CharField(max_length=300,  blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]


class Photo(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True, upload_to=content_file_name('profile_photo/'))

    def __str__(self):
        return self.UserId.username