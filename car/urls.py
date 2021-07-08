from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from car import views
#
# router = routers.DefaultRouter()
# router.register('', views.HomeAndFilter)

urlpatterns = [
    # path('', include(router.urls), name='home'),
    path('', views.CarList.as_view(), name='home'),
    path('mycar/', views.MyCarList.as_view(), name='mycar'),
    path('myrentedcar/', views.MyRentedCarList.as_view(), name='myrentedcar'),
    path('register/', views.CarRegister.as_view(), name='register'),
    path('bookcar/', views.BookCar.as_view(), name='bookcar'),
    path('feedback/', views.FeedbackCar.as_view(), name='feedback'),
    path('cancel/', views.CancelBookedCar.as_view(), name='cancel'),

]
