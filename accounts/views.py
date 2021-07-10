from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Photo, User
from .serializer import UserDetailsSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from knox.views import LoginView as KnoxLoginView
from .serializer import RegisterSerializer, UserSerializer, ChangePasswordSerializer, LogoutSerializer, PhotoSerializer, UserUpdateSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework import generics, mixins, permissions
import json
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            print(request.data)
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response({'id': user.id, 'username': user.username, 'email': user.email, 'token': json},
                                status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     return Response({
    #         "user": UserSerializer(user, context=self.get_serializer_context()).data,
    #     })

#
# class UpdateAndDelete(generics.GenericAPIView):   ####
#     serializer_class = RegisterSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def put(self, request):
#         print(request)
#         user = request.user
#         try:
#             u = User.objects.get(id=user.id)
#             print(u)
#             # u = User.objects.get(id=user)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         if request.method == "PUT":
#             serializer = RegisterSerializer(data=request.data)
#             data = {}
#             if serializer.is_valid():
#                 serializer.save(request)
#                 data['success'] = "update successful"
#                 return Response(data=data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class UserProfileChangeAPIView(generics.RetrieveAPIView,
                               mixins.DestroyModelMixin,
                               mixins.UpdateModelMixin):
    permission_classes = (
        permissions.IsAuthenticated,
        UserIsOwnerOrReadOnly,
    )
    serializer_class = UserUpdateSerializer

    def get_queryset(self):
        user = self.request.user.id
        return User.objects.filter(id=user)
    # def get_object(self):
    #     username = self.kwargs["username"]
    #     obj = get_object_or_404(User, username=username)
    #     return obj

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # def delete(self, request):
    #     user = request.user
    #     try:
    #         u = User.objects.get(UserId=user)
    #     except User.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    #     if request.method == "DELETE":
    #         operation = u.delete()
    #         data = {}
    #         if operation:
    #             data["success"] = "delete successful"
    #         else:
    #             data["failure"] = "delete failed"
    #         return Response(data=data)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


#
# class LogoutAPI(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request, format=None):
#         # simply delete the token to force a login
#         print(request.user.Bearer)
#         if request.user.Bearer:
#             request.user.Bearer.delete()
#             return Response({"Logout Done."}, status=status.HTTP_200_OK)
#         else:
#             return Response({"No token found."})
#
#
# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class ChangePasswordView(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    # authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotoSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(UserId=user)
            if photo:
                return Response({'id': photo.id, 'message': 'Photo Added'}, status=status.HTTP_201_CREATED)
        return Response({"error": "photo already exist in database, you can just update it or delete it."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        try:
            u = Photo.objects.get(UserId=user)
        except Photo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = PhotoSerializer(u, data=request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data['success'] = "update successful"
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # serializer = self.serializer_class(data=request.data)
        # payload = json.loads(request.body)
        # if serializer.is_valid():
        #     p = Photo.objects.filter(UserId=user)
        #     photo =
        #     if photo:
        #         return Response({'id': photo.id, 'message': 'Photo Updated'}, status=status.HTTP_201_CREATED)
        # return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        try:
            u = Photo.objects.get(UserId=user)
        except Photo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            operation = u.delete()
            data = {}
            if operation:
                data["success"] = "delete successful"
            else:
                data["failure"] = "delete failed"
            return Response(data=data)
