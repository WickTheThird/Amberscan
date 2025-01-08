from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import *

class SerializeLoginClient(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password. Please try again.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        return {
            "username": user.username,
            "password": password,
        }


class SerializeSignInClient(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
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
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )


class SerializeImages(serializers.ModelSerializer):
    provider = serializers.CharField()
    client = serializers.CharField()

    class Meta:
        model = Images
        fields = ['provider', 'client', 'name', 'image']

    def validate_image(self, value):
        allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif')
        if not value.name.lower().endswith(allowed_extensions):
            raise serializers.ValidationError(f"Uploaded file must be an image with extensions: {', '.join(allowed_extensions)}.")
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image size must not exceed 5MB.")
        return value

    def validate_provider(self, value):
        if isinstance(value, Providers):
            return value

        try:
            provider = Providers.objects.get(signature=value, is_active=True)
            return provider
        except Providers.DoesNotExist:
            raise serializers.ValidationError(f"Provider with signature '{value}' does not exist or is inactive.")

    def validate_client(self, value):
        try:
            client = User.objects.get(username=value)
            return client
        except User.DoesNotExist:
            raise serializers.ValidationError(f"Client with username '{value}' does not exist.")

    def validate(self, data):
        provider = self.validate_provider(data['provider'])
        client = self.validate_client(data['client'])

        if provider.client != client:
            raise serializers.ValidationError("The specified provider does not belong to the specified client.")

        data['provider'] = provider
        data['client'] = client

        return data


class SerializePDF(serializers.ModelSerializer):
    provider = serializers.CharField()
    client = serializers.CharField()

    class Meta:
        model = PDFs
        fields = ['provider', 'client', 'name', 'pdf']

    def validate_pdf(self, value):
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Uploaded file must be a PDF.")
        # Uncomment if needed for file size validation:
        # if value.size > 10 * 1024 * 1024:  # 10MB limit
        #     raise serializers.ValidationError("PDF size must not exceed 10MB.")
        return value

    def validate_provider(self, value):
        if isinstance(value, Providers):
            return value

        try:
            provider = Providers.objects.get(signature=value, is_active=True)
            return provider
        except Providers.DoesNotExist:
            raise serializers.ValidationError(f"Provider with signature '{value}' does not exist or is inactive.")

    def validate_client(self, value):
        try:
            client = User.objects.get(username=value)
            return client
        except User.DoesNotExist:
            raise serializers.ValidationError(f"Client with username '{value}' does not exist.")

    def validate(self, data):
        provider = self.validate_provider(data['provider'])
        client = self.validate_client(data['client'])

        if provider.client != client:
            raise serializers.ValidationError("The specified provider does not belong to the specified client.")

        data['provider'] = provider
        data['client'] = client

        return data
