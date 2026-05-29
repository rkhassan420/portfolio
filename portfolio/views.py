from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import HomeInfo, AboutInfo, FooterInfo, ProjectsInfo, OTPVerification
from .serializer import HomeSerializer, AboutSerializer, FooterSerializer, ProjectsSerializer
from .utils import generate_otp, send_otp_email


# ─────────────────────────────────────────────
#  OTP
# ─────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def SendOTPView(request):
    email = request.data.get('email', '').strip()

    if not email:
        return Response({'error': 'Email is required'}, status=400)
    if '@' not in email or '.' not in email:
        return Response({'error': 'Invalid email format'}, status=400)

    otp = generate_otp()
    OTPVerification.objects.filter(email=email).delete()
    OTPVerification.objects.create(email=email, otp=otp)

    try:
        send_otp_email(email, otp)
        return Response({'message': 'OTP sent successfully'}, status=200)
    except Exception as e:
        return Response({'error': f'Failed to send OTP: {str(e)}'}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def VerifyOTPView(request):
    email = request.data.get('email', '').strip()
    otp   = request.data.get('otp', '').strip()

    if not email or not otp:
        return Response({'error': 'Email and OTP are required'}, status=400)

    try:
        record = OTPVerification.objects.filter(
            email=email, otp=otp, is_verified=False
        ).latest('created_at')

        if record.is_expired():
            return Response({'error': 'OTP has expired. Please request a new one.'}, status=400)

        record.is_verified = True
        record.save()
        return Response({'message': 'OTP verified successfully'}, status=200)

    except OTPVerification.DoesNotExist:
        return Response({'error': 'Invalid OTP. Please try again.'}, status=400)


# ─────────────────────────────────────────────
#  AUTH — JWT (no CSRF needed)
# ─────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def JWTRegisterView(request):
    username = request.data.get('username', '').strip()
    email    = request.data.get('email', '').strip()
    password = request.data.get('password', '')

    if not all([username, email, password]):
        return Response({'error': 'All fields are required'}, status=400)
    if len(username) < 3:
        return Response({'error': 'Username must be at least 3 characters'}, status=400)
    if not username.replace('_', '').isalnum():
        return Response({'error': 'Username can only contain letters, numbers, underscores'}, status=400)
    if len(password) < 6:
        return Response({'error': 'Password must be at least 6 characters'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=400)

    user = User(username=username, email=email)
    user.set_password(password)
    user.save()

    refresh = RefreshToken.for_user(user)
    return Response({
        'message':  'Account created successfully',
        'username': user.username,
        'access':   str(refresh.access_token),
        'refresh':  str(refresh),
    }, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def JWTLoginView(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '')

    if not all([username, password]):
        return Response({'error': 'Username and password are required'}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'message':  'Login successful',
            'username': user.username,
            'access':   str(refresh.access_token),
            'refresh':  str(refresh),
        }, status=200)
    else:
        return Response({'error': 'Invalid username or password'}, status=401)


@api_view(['POST'])
@permission_classes([AllowAny])
def RefreshTokenView(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({'error': 'Refresh token required'}, status=400)
    try:
        refresh = RefreshToken(refresh_token)
        return Response({'access': str(refresh.access_token)}, status=200)
    except Exception:
        return Response({'error': 'Invalid or expired refresh token'}, status=401)


# ─────────────────────────────────────────────
#  HOME INFO
# ─────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def get_home_info(request):
    username = request.query_params.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=400)
    try:
        obj = HomeInfo.objects.get(username=username)
        return Response(HomeSerializer(obj).data)
    except HomeInfo.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_home_info(request):
    username = request.data.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=400)

    try:
        obj  = HomeInfo.objects.get(username=username)
        data = request.data.copy()
        if not data.get('image'): data['image'] = obj.image
        if not data.get('cv'):    data['cv']    = obj.cv
        serializer = HomeSerializer(obj, data=data, partial=True)
    except HomeInfo.DoesNotExist:
        serializer = HomeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


# ─────────────────────────────────────────────
#  ABOUT INFO
# ─────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def get_about_info(request):
    username = request.query_params.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=400)
    try:
        obj = AboutInfo.objects.get(username=username)
        return Response(AboutSerializer(obj).data)
    except AboutInfo.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_about_info(request):
    username = request.data.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=400)

    try:
        obj  = AboutInfo.objects.get(username=username)
        data = request.data.copy()
        if not data.get('image'): data['image'] = obj.image
        serializer = AboutSerializer(obj, data=data, partial=True)
    except AboutInfo.DoesNotExist:
        serializer = AboutSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


# ─────────────────────────────────────────────
#  FOOTER INFO
# ─────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def get_footer_info(request):
    username = request.query_params.get('username')
    if not username:
        return Response({'error': 'Username is required'}, status=400)
    try:
        objs = FooterInfo.objects.filter(username=username)
        return Response(FooterSerializer(objs, many=True).data, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def add_footer_info(request):
    username = request.data.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=400)

    try:
        obj  = FooterInfo.objects.get(username=username)
        data = request.data.copy()
        serializer = FooterSerializer(obj, data=data, partial=True)
    except FooterInfo.DoesNotExist:
        serializer = FooterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


# ─────────────────────────────────────────────
#  PROJECTS INFO
# ─────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def get_projects_info(request):
    username = request.query_params.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=400)

    objs = ProjectsInfo.objects.filter(username=username).order_by('-id')
    return Response({'data': ProjectsSerializer(objs, many=True).data, 'count': objs.count()})


@api_view(['POST'])
@permission_classes([AllowAny])
def add_projects_info(request):
    username = request.data.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=400)

    serializer = ProjectsSerializer(data=request.data.copy())
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_projects_info(request, pk):
    try:
        ProjectsInfo.objects.get(pk=pk).delete()
        return Response(status=204)
    except ProjectsInfo.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)


# ─────────────────────────────────────────────
#  ACCOUNT
# ─────────────────────────────────────────────

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_user_account(request, username):
    try:
        User.objects.get(username=username).delete()
        return Response({'message': 'User deleted successfully'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
