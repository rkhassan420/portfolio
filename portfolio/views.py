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
from .models import PortfolioVisit
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta


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
    otp = request.data.get('otp', '').strip()

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
    email = request.data.get('email', '').strip()
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
        'message': 'Account created successfully',
        'username': user.username,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
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
            'message': 'Login successful',
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
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
        obj = HomeInfo.objects.get(username=username)
        data = request.data.copy()
        if not data.get('image'): data['image'] = obj.image
        if not data.get('cv'):    data['cv'] = obj.cv
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
        obj = AboutInfo.objects.get(username=username)
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
        obj = FooterInfo.objects.get(username=username)
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


# ─────────────────────────────────────────────
#  ANALYTICS
# ─────────────────────────────────────────────


@api_view(['POST'])
@permission_classes([AllowAny])
def track_visit(request):
    """Called automatically when someone opens a portfolio page."""
    username = request.data.get('username', '').strip()
    if not username:
        return Response({'error': 'Username required'}, status=400)

    PortfolioVisit.objects.create(
        username=username,
        country=request.data.get('country', ''),
        device=request.data.get('device', ''),
        browser=request.data.get('browser', ''),
        section=request.data.get('section', 'home'),
    )
    return Response({'message': 'Visit tracked'}, status=201)


@api_view(['GET'])
@permission_classes([AllowAny])
# def get_analytics(request):
#     username = request.query_params.get('username', '').strip()
# ✅ New code
def get_analytics(request, username):  # username comes from URL
    username = username.strip()
    if not username:
        return Response({'error': 'Username required'}, status=400)

    visits = PortfolioVisit.objects.filter(username=username)

    # ── Totals ──
    total_visits = visits.count()

    # ── Last 7 days visits per day ──
    seven_days_ago = timezone.now() - timedelta(days=6)
    daily = (
        visits.filter(visited_at__gte=seven_days_ago)
        .annotate(date=TruncDate('visited_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # Fill in missing days with 0
    daily_map = {str(d['date']): d['count'] for d in daily}
    daily_data = []
    for i in range(7):
        day = (timezone.now() - timedelta(days=6 - i)).date()
        daily_data.append({
            'date': str(day),
            'label': day.strftime('%a'),
            'count': daily_map.get(str(day), 0),
        })

    # ── Today vs Yesterday ──
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    today_count = visits.filter(visited_at__date=today).count()
    yesterday_count = visits.filter(visited_at__date=yesterday).count()

    # ── Top countries ──
    countries = (
        visits.exclude(country='')
        .values('country')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    # ── Device breakdown ──
    devices = (
        visits.exclude(device='')
        .values('device')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # ── Browser breakdown ──
    browsers = (
        visits.exclude(browser='')
        .values('browser')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    # ── This month vs last month ──
    this_month = timezone.now().replace(day=1)
    last_month = (this_month - timedelta(days=1)).replace(day=1)
    this_month_count = visits.filter(visited_at__gte=this_month).count()
    last_month_count = visits.filter(
        visited_at__gte=last_month,
        visited_at__lt=this_month
    ).count()

    return Response({
        'total_visits': total_visits,
        'today_visits': today_count,
        'yesterday_visits': yesterday_count,
        'this_month_visits': this_month_count,
        'last_month_visits': last_month_count,
        'daily_data': daily_data,
        'top_countries': list(countries),
        'devices': list(devices),
        'browsers': list(browsers),
    }, status=200)


# ─────────────────────────────────────────────
#  OAUTH — Google & GitHub
# ─────────────────────────────────────────────

import requests as http_requests
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def _jwt_for_user(user):
    """Helper — returns JWT tokens dict for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        'username': user.username,
        'email': user.email,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def GoogleOAuthView(request):
    """
    Receives a Google access_token from frontend.
    Verifies it with Google, finds or creates the user, returns JWT.
    """
    access_token = request.data.get('access_token', '').strip()
    if not access_token:
        return Response({'error': 'access_token is required'}, status=400)

    # Verify token with Google
    try:
        google_resp = http_requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=10,
        )
        if google_resp.status_code != 200:
            return Response({'error': 'Invalid Google token'}, status=401)

        google_data = google_resp.json()
    except Exception:
        return Response({'error': 'Failed to verify Google token'}, status=500)

    email = google_data.get('email', '').strip()
    name = google_data.get('name', '')
    google_id = google_data.get('sub', '')  # unique Google user ID

    if not email:
        return Response({'error': 'Could not retrieve email from Google'}, status=400)

    # Find or create user
    # Username = first part of email, made unique if needed
    base_username = email.split('@')[0].replace('.', '_').lower()
    user = User.objects.filter(email=email).first()

    if not user:
        username = base_username
        # Make username unique
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create(
            username=username,
            email=email,
            first_name=name.split()[0] if name else '',
            last_name=' '.join(name.split()[1:]) if name and len(name.split()) > 1 else '',
        )
        user.set_unusable_password()  # OAuth users don't have passwords
        user.save()

    return Response({'message': 'Google login successful', **_jwt_for_user(user)}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def GitHubOAuthView(request):
    """
    Receives a GitHub code from frontend (after OAuth redirect).
    Exchanges code for access_token, fetches user info, returns JWT.
    """
    code = request.data.get('code', '').strip()
    if not code:
        return Response({'error': 'code is required'}, status=400)

    client_id = request.data.get('client_id', '').strip()
    client_secret = request.data.get('client_secret', '').strip()

    if not client_id or not client_secret:
        return Response({'error': 'client_id and client_secret required'}, status=400)

    # Exchange code for access token
    try:
        token_resp = http_requests.post(
            'https://github.com/login/oauth/access_token',
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
            },
            headers={'Accept': 'application/json'},
            timeout=10,
        )
        token_data = token_resp.json()
        access_token = token_data.get('access_token')

        if not access_token:
            return Response({'error': 'Failed to get GitHub access token'}, status=401)

    except Exception:
        return Response({'error': 'Failed to contact GitHub'}, status=500)

    # Get user info
    try:
        user_resp = http_requests.get(
            'https://api.github.com/user',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/vnd.github.v3+json',
            },
            timeout=10,
        )
        github_data = user_resp.json()

        # GitHub may hide email — fetch primary email separately
        email = github_data.get('email')
        if not email:
            emails_resp = http_requests.get(
                'https://api.github.com/user/emails',
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Accept': 'application/vnd.github.v3+json',
                },
                timeout=10,
            )
            emails = emails_resp.json()
            primary = next((e for e in emails if e.get('primary') and e.get('verified')), None)
            email = primary['email'] if primary else None

    except Exception:
        return Response({'error': 'Failed to fetch GitHub user info'}, status=500)

    github_login = github_data.get('login', '')  # GitHub username
    name = github_data.get('name', '') or github_login

    if not email and not github_login:
        return Response({'error': 'Could not retrieve user info from GitHub'}, status=400)

    # Find or create user — prefer matching by email, fallback to github username
    user = None
    if email:
        user = User.objects.filter(email=email).first()

    if not user:
        user = User.objects.filter(username=github_login).first()

    if not user:
        # Create new user
        base_username = github_login or (email.split('@')[0] if email else 'user')
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create(
            username=username,
            email=email or '',
            first_name=name.split()[0] if name else '',
            last_name=' '.join(name.split()[1:]) if name and len(name.split()) > 1 else '',
        )
        user.set_unusable_password()
        user.save()

    return Response({'message': 'GitHub login successful', **_jwt_for_user(user)}, status=200)
