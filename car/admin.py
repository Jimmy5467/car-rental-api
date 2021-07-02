from django.contrib import admin
# Register your models here.
from .models import Car, Cancel, Feedback, Booked

admin.site.register(Car)
admin.site.register(Cancel)
admin.site.register(Feedback)
admin.site.register(Booked)