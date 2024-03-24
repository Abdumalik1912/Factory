from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "password", "first_name", "last_name", "phone_number", "city",
                  "confirmed_date", "update_date"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user
