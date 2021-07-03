from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import Car, Cancel, Feedback, Booked
from .serializers import ShowCarSerializer, CarRegisterSerializer, BookCarSerializer, FeedbackSerializer, CancelSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


# Create your views here.
class CarRegister(APIView):
    serializer_class = CarRegisterSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            car = serializer.save(ownerId=user)
            if car:
                return Response({'Car registered. You can check by login again.'}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCar(APIView):
    serializer_class = BookCarSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            car = serializer.save(renterId=user, renter_phone=user.phone)
            if car:
                return Response({'Car Booking done.'}, status=status.HTTP_201_CREATED)

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

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            car = serializer.save(renterId=user)
            print(serializer)
            if car:
                return Response({'Booking canceled.'}, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

