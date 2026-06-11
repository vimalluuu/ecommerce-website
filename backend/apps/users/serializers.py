"""
Users app serializers.
"""

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Address


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for user addresses."""

    class Meta:
        model = Address
        fields = [
            'id', 'label', 'street', 'city', 'state',
            'postal_code', 'country', 'is_default', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_postal_code(self, value):
        if not value.strip():
            raise serializers.ValidationError("Postal code cannot be empty.")
        return value.strip()


class UserSerializer(serializers.ModelSerializer):
    """Full user profile serializer (read/update)."""

    addresses = AddressSerializer(many=True, read_only=True)
    total_orders = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'phone', 'avatar_url',
            'is_admin', 'is_email_verified', 'date_joined', 'addresses', 'total_orders',
        ]
        read_only_fields = ['id', 'email', 'is_admin', 'is_email_verified', 'date_joined']

    def get_total_orders(self, obj):
        return obj.orders.count()


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile fields."""

    class Meta:
        model = User
        fields = ['name', 'phone', 'avatar_url']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value.strip()

    def validate_phone(self, value):
        if value and not value.replace('+', '').replace(' ', '').replace('-', '').isdigit():
            raise serializers.ValidationError("Enter a valid phone number.")
        return value.strip()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password', 'password_confirm']

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value.lower()

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Full name is required.")
        return value.strip()

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        try:
            validate_password(attrs['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            phone=validated_data.get('phone', ''),
            password=validated_data['password'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for login — validates credentials and returns JWT tokens."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        from django.contrib.auth import authenticate
        email = attrs.get('email', '').lower()
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password. Please try again.")
        if not user.is_active:
            raise serializers.ValidationError("Your account has been deactivated. Contact support.")

        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    """Serializer for logout — requires refresh token to blacklist it."""

    refresh = serializers.CharField()

    def validate_refresh(self, value):
        if not value.strip():
            raise serializers.ValidationError("Refresh token is required.")
        return value.strip()


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for requesting a password reset email."""

    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower().strip()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming a password reset with a token."""

    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "Passwords do not match."})
        try:
            validate_password(attrs['new_password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return attrs


class EmailVerifySerializer(serializers.Serializer):
    """Serializer for verifying an email address using a token."""

    token = serializers.CharField()

    def validate_token(self, value):
        if not value.strip():
            raise serializers.ValidationError("Verification token is required.")
        return value.strip()
