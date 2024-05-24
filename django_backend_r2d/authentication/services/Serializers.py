from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from framework.utils.EmailHandler import EmailHandler
from django.contrib.auth import get_user_model
User = get_user_model() 

class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomTokenPairSerializer(TokenObtainPairSerializer):
    """Serializer for JWT Tokens add more fields in the get_token method to append information to JWT Tokens"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['preferred_name'] = user.preferred_name
        token['email'] = EmailHandler.mask_email(user.email)
        token['role'] = user.role
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenPairSerializer