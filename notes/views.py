# views.py
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Note, PasswordResetCode
from .serializers import NoteSerializer
from .serializers import UserSerializer


# Register
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login
from django.contrib.auth import authenticate


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": {"id": user.id, "username": user.username, "email": user.email},
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)





class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)





class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")

        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate 4-digit code
        code = str(random.randint(1000, 9999))

        # Store in DB
        PasswordResetCode.objects.create(user=user, code=code)

        # Send email
        send_mail(
            subject="Password Reset Code",
            message=f"Your reset code is {code}",
            from_email="yourgmail@gmail.com",
            recipient_list=[user.email],
        )

        return Response({
            "message": "Reset code sent",
            "email": user.email
        }, status=status.HTTP_200_OK)



class VerifyCodeView(APIView):
        permission_classes = [AllowAny]
        def post(self, request):
            username = request.data.get("username")
            code = request.data.get("code")

            if not username or not code:
                return Response({"error": "Username and code are required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                reset_code = PasswordResetCode.objects.filter(user=user, code=code).latest("created_at")
            except PasswordResetCode.DoesNotExist:
                return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

            if reset_code.is_expired():
                return Response({"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Code verified successfully"}, status=status.HTTP_200_OK)




class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        new_password = request.data.get("password")

        if not username or not new_password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Set the new password securely
        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)




class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def delete(self, request, user_id):
        token_user = request.user
        if token_user.id != user_id:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
            # delete all notes of this user
            Note.objects.filter(user=user).delete()
            # delete user
            user.delete()
            return Response({"message": "User and notes deleted successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

