from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()

"""
Serializer for user registration.
Validates that the username and email are unique, and ensures that the password 
matches the confirm password field during registration.
"""


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "confirm_password", "email"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists.")
        return value

    def validate(self, data):
        print(data)
        if data["password"] != data["confirm_password"]:
            raise ValidationError({"confirm_password": "Passwords does not match."})
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            return user
        raise serializers.ValidationError("Invalid credentials")


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
