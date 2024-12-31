from rest_framework import serializers
from rest_framework.response import Response

from django.contrib.auth.hashers import make_password

from .models import *

class SerializeLoginClient(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = Clients.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        return data


class SerializeSignInClient(serializers.ModelSerializer):
    
    class Meta:
        model = Clients
        fields = ['name', 'email', 'password']
        
    def validate_email(self, value):
        if Clients.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)



class SerializeImages(serializers.ModelSerializer):
    
    class Meta:
        model = Images
        fields = ['provider', 'client', 'name', 'image']

class SerializePDF(serializers.ModelSerializer):
    
    class Meta:
        model = PDFs
        fields = ['provider', 'client', 'name', 'pdf']
