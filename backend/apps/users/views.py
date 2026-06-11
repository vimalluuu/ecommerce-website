"""
Users app views — Auth endpoints and profile management.
"""

import logging
import secrets

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Address
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserSerializer,
    UserUpdateSerializer,
    AddressSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerifySerializer,
)

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    """
    POST /api/auth/register/
    Register a new user and send a verification email.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        # Generate email verification token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verify_url = f"{settings.FRONTEND_URL}/verify-email?uid={uid}&token={token}"

        try:
            send_mail(
                subject="Verify your ARCFORM account",
                message=(
                    f"Welcome to ARCFORM, {user.name}!\n\n"
                    f"Please verify your email address by clicking the link below:\n"
                    f"{verify_url}\n\n"
                    f"If you did not create an account, ignore this email."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception as exc:
            logger.warning("Failed to send verification email to %s: %s", user.email, exc)

        # Return JWT tokens for immediate login after registration
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "success": True,
                "message": "Account created. Please verify your email.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    POST /api/auth/login/
    Authenticate user and return JWT pair.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        validated = serializer.validated_data
        user = validated['user']

        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "access": validated['access'],
                "refresh": validated['refresh'],
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Blacklist the provided refresh token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(serializer.validated_data['refresh'])
            token.blacklist()
        except TokenError as exc:
            return Response(
                {"success": False, "message": f"Invalid or expired refresh token: {exc}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"success": True, "message": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestView(APIView):
    """
    POST /api/auth/password/reset/
    Send password reset email.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data['email']
        # Always return 200 to avoid user enumeration attacks
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"

            send_mail(
                subject="Reset your ARCFORM password",
                message=(
                    f"Hi {user.name},\n\n"
                    f"We received a request to reset your ARCFORM password.\n"
                    f"Click the link below to reset it:\n{reset_url}\n\n"
                    f"This link expires in 1 hour.\n"
                    f"If you did not request this, ignore this email."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except User.DoesNotExist:
            pass
        except Exception as exc:
            logger.warning("Failed to send password reset email: %s", exc)

        return Response(
            {"success": True, "message": "If that email is registered, a reset link has been sent."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    """
    POST /api/auth/password/reset/confirm/
    Confirm password reset with uid + token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        from .serializers import PasswordResetConfirmSerializer
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        uid_b64 = request.data.get('uid', '')
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            uid = force_str(urlsafe_base64_decode(uid_b64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, OverflowError):
            return Response(
                {"success": False, "message": "Invalid reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"success": False, "message": "Reset link is invalid or has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save(update_fields=['password'])

        return Response(
            {"success": True, "message": "Password reset successfully. You can now log in."},
            status=status.HTTP_200_OK,
        )


class EmailVerifyView(APIView):
    """
    POST /api/auth/email/verify/
    Verify email address using uid + token from the verification email.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        uid_b64 = request.data.get('uid', '')
        token = serializer.validated_data['token']

        try:
            uid = force_str(urlsafe_base64_decode(uid_b64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, OverflowError):
            return Response(
                {"success": False, "message": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_email_verified:
            return Response(
                {"success": True, "message": "Email is already verified."},
                status=status.HTTP_200_OK,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"success": False, "message": "Verification link is invalid or has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_email_verified = True
        user.save(update_fields=['is_email_verified'])

        return Response(
            {"success": True, "message": "Email verified successfully."},
            status=status.HTTP_200_OK,
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/auth/profile/ — Return authenticated user profile.
    PUT  /api/auth/profile/ — Update user profile fields.
    PATCH /api/auth/profile/ — Partial update.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response({"success": True, "user": serializer.data})


class AddressListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/auth/addresses/ — List all addresses for authenticated user.
    POST /api/auth/addresses/ — Create a new address.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"success": True, "addresses": serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_create(serializer)
        return Response(
            {"success": True, "message": "Address added.", "address": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/auth/addresses/<uuid:pk>/ — Retrieve address.
    PUT    /api/auth/addresses/<uuid:pk>/ — Update address.
    PATCH  /api/auth/addresses/<uuid:pk>/ — Partial update.
    DELETE /api/auth/addresses/<uuid:pk>/ — Delete address.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response({"success": True, "address": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"success": True, "message": "Address deleted."},
            status=status.HTTP_200_OK,
        )
