# ✅ Use the custom user model instead of the default 'auth.User'
from django.contrib.auth import get_user_model
User = get_user_model()  # 🔄 Replaces: from django.contrib.auth.models import User

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# ✅ Removed duplicate import
# from rest_framework.views import APIView
# from rest_framework.response import Response

from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]  # ✅ Ensures public access despite global IsAuthenticated default
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # ✅ Typo fix: "massage" → "message"
            return Response({"message": "If this email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

        # ✅ Token and UID generation for secure reset link
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # ✅ Use settings or reverse() for dynamic domain in production
        reset_link = f"http://192.168.1.208:8000/reset-password-confirm/?uid={uid}&token={token}"

        # ✅ Use DEFAULT_FROM_EMAIL from settings
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=None,  # 🔄 Consider using settings.DEFAULT_FROM_EMAIL
            recipient_list=[email],
        )

        print("mail sent to user")  

        return Response({"message": "If this email exists, a reset link has been sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]  # ✅ Allows unauthenticated access for token-based reset
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
