from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


# -----------------------------
# USER SERIALIZER
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'country', 'date_joined',]
        read_only_fields = ['id', 'date_joined']


# -----------------------------
# USER REGISTRATION SERIALIZER
# -----------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'country', 'password']

    def validate_username(self, value):
        value = value.lower()
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# -----------------------------
# USER LOGIN SERIALIZER
# -----------------------------    
class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})


# -----------------------------
# USER CHANGE OF PASSWORD SERIALIZER
# -----------------------------
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])


# -----------------------------
# USER PROFILE UPDATE SERIALIZER
# -----------------------------
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'country']