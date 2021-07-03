from rest_framework import serializers
from .models import Cancel, Car, Booked, Feedback
from accounts.models import User


class CarRegisterSerializer(serializers.ModelSerializer):
    ownerId = serializers.PrimaryKeyRelatedField(read_only=True)
    # ownerId = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Car
        fields = ['ownerId', 'company', 'car_model_name', 'seats', 'car_type', 'fuel', 'rent', 'number_plate', 'issue', 'city', 'pickup_address',
                  'drop_address', 'available_from', 'availability_ends', 'rc_number', 'AC', 'AorM', 'front_image', 'back_image']

    # def save(self, **kwargs):
    #     kwargs["ownerId"] = self.fields["ownerId"].get_default()
    #     return super().save(**kwargs)


class BookCarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booked
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = "__all__"


class CancelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cancel
        fields = "__all__"


class ShowCarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'