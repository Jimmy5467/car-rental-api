from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import Car, Cancel, Feedback, Booked
from .serializers import ShowCarSerializer, CarRegisterSerializer, BookCarSerializer, FeedbackSerializer, CancelSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from django.db.models import Q
import datetime


class CarFilter(filters.FilterSet):
    # company = filters.CharFilter(lookup_expr='icontains')
    # car_model_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Car
        fields = {                      # iexact
            'company': ['icontains'],
            'car_model_name': ['icontains'],
            'city': ['icontains'],
            'seats': ['lte', 'gte'],
            'rent': ['lte', 'gte'],

        }


class CarList(ListAPIView):
    today = datetime.datetime.today()
    queryset = Car.objects.filter(Q(availability_ends__gte=today) & Q(available_from__lte=today))
    permission_classes = (AllowAny,)
    serializer_class = ShowCarSerializer
    filterset_class = CarFilter
    # filter_fields = ['company']


# Create your views here.
class CarRegister(APIView):
    serializer_class = CarRegisterSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            car = serializer.save(ownerId=user)
            if car:
                return Response({'id': car.id, 'number_plate': car.number_plate, 'model': car.car_model_name, 'message' : 'Car Registered'}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCar(APIView):
    serializer_class = BookCarSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            car = serializer.save(renterId=user)
            if car:
                return Response({'car id': car.id, 'message': 'Car Booked '}, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackCar(APIView):
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            car = serializer.save()
            if car:
                return Response({'Thank you for feedback'}, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelBookedCar(APIView):
    serializer_class = CancelSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            car = serializer.save(renterId=user)
            if car:
                return Response({'Booking canceled.'}, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyCarList(ListAPIView):
    queryset = Car.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ShowCarSerializer

    def get_queryset(self):
        user = self.request.user
        return Car.objects.filter(ownerId=user)


class MyRentedCarList(ListAPIView):
    # queryset = Booked.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BookCarSerializer

    def get_queryset(self):
        user = self.request.user
        return Booked.objects.filter(renterId=user)

# class CarFilter(filters.FilterSet):
#
#     class Meta:
#         model = Car
#         fields = {
#             'company': ['icontains'],
#             'seats': ['iexact', 'lte', 'gte']
#         }

#
# class HomeAndFilter(viewsets.ModelViewSet):
#     queryset = Car.objects.all()
#     serializer_class = ShowCarSerializer
#     filter_backends = (DjangoFilterBackend, OrderingFilter)
#     filter_fields = ('company', 'seats', )
#     ordering_fields = ('company', 'seats ', )
#     ordering = ('seats', )
#     search_fields = ('car_type', 'rent', 'number_plate')

    # filterset_class = CarFilter
    #
    # def carfilter(self, request):
    #     car = request.get_queryset().order_by('company').last()
    #     serializer = request.get_serializer_class()(HomeAndFilter)
    #     return Response(serializer.data)

