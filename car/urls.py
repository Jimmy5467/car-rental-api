from django.urls import path, include
from django.contrib import admin
from car import views


urlpatterns = [
    path('register/', views.CarRegister.as_view(), name='home'),
    path('bookcar/', views.BookCar.as_view(), name='home'),
    path('feedback/', views.FeedbackCar.as_view(), name='home'),
    path('cancel/', views.CancelBookedCar.as_view(), name='home'),
]
