from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Car, Cancel, Feedback, Booked
from .serializers import CarRegisterSerializer, BookCarSerializer, FeedbackSerializer, CancelSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class CarRegister(APIView):
    serializer_class = CarRegisterSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            car = serializer.save()
            if car:
                return Response({'Car registered. You can check by login again.'}, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCar(APIView):
    serializer_class = BookCarSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            car = serializer.save()
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
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            car = serializer.save()
            if car:
                return Response({'Booking canceled.'}, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)