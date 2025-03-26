import random
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, AuthToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, VerifyOTPSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp_code = str(random.randint(100000, 999999))
            user.otp_code = otp_code
            user.save()
            send_mail('Your OTP Code', f'Your OTP is {otp_code}', 'noreply@example.com', [user.email])
            return Response({'message': 'OTP sent'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, email=serializer.validated_data['email'])
            if user.otp_code == serializer.validated_data['otp_code']:
                user.is_verified = True
                user.otp_code = None
                user.save()
                return Response({'message': 'Account verified'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user and user.is_verified:
                login(request, user)
                token, _ = AuthToken.objects.get_or_create(user=user)
                response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                response.set_cookie('auth_token', str(token.token), httponly=True, secure=True)
                return response
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response({'message': 'Logged out'}, status=status.HTTP_200_OK)
        response.delete_cookie('auth_token')
        return response
