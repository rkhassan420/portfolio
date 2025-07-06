from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import HomeInfo, AboutInfo, FooterInfo, ProjectsInfo, LatestInfo
from .serializer import HomeSerializer, AboutSerializer, FooterSerializer, ProjectsSerializer, LatestSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie  # ← this is directly usable here
def GetCrsfToken(request):
    return Response({'success': 'CSRF Cookie Set'})


@csrf_protect
@api_view(['POST'])
@permission_classes([AllowAny])
def RegisterView(request):
    data = request.data

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)

    user = User(username=username, email=email)
    user.set_password(password)  # Securely hash the password
    user.save()

    return Response({'message': 'User registered successfully'}, status=201)


@csrf_protect
@api_view(['POST'])
@permission_classes([AllowAny])
def LoginView(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)  # ✅ Creates session ID and sends it in cookie
        request.session['username'] = user.username
        return Response({'message': 'Login successful', 'username': user.username}, status=200)
    else:
        return Response({'error': 'Invalid username or password'}, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def LogoutView(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_home_info(request):
    username = request.query_params.get('username')

    if not username:
        return Response({"error": "Username is required"}, status=400)

    try:
        home_info = HomeInfo.objects.get(username=username)
        serializer = HomeSerializer(home_info)
        return Response(serializer.data)
    except HomeInfo.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# get HomeInfo


@api_view(['POST'])
@permission_classes([AllowAny])
def add_home_info(request):
    username = request.data.get('username')

    if not username:
        return Response({"error": "Username is required"}, status=400)

    try:
        home_info = HomeInfo.objects.get(username=username)

        # ✅ Create a mutable copy of request data
        data = request.data.copy()

        # ✅ If image or cv not provided, keep the existing ones
        if not data.get('image'):
            data['image'] = home_info.image
        if not data.get('cv'):
            data['cv'] = home_info.cv

        serializer = HomeSerializer(home_info, data=data, partial=True)

    except HomeInfo.DoesNotExist:
        serializer = HomeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)


# post HomeInfo


# get AboutInfo

@api_view(['GET'])
@permission_classes([AllowAny])
def get_about_info(request):
    username = request.query_params.get('username')

    if not username:
        return Response({"error": "Username is required"}, status=400)

    try:
        about_info = AboutInfo.objects.get(username=username)
        serializer = AboutSerializer(about_info)
        return Response(serializer.data)
    except HomeInfo.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# get AboutInfo


# post AboutInfo

@api_view(['POST'])
@permission_classes([AllowAny])
def add_about_info(request):
    username = request.data.get('username')

    if not username:
        return Response({"error": "Username is required"}, status=400)

    try:
        about_info = AboutInfo.objects.get(username=username)

        # ✅ Create a mutable copy of request data
        data = request.data.copy()

        # ✅ If image or cv not provided, keep the existing ones
        if not data.get('image'):
            data['image'] = about_info.image

        serializer = AboutSerializer(about_info, data=data, partial=True)


    except AboutInfo.DoesNotExist:
        serializer = AboutSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)


# post AboutInfo


# post LatestInfo

@api_view(['POST'])
@permission_classes([AllowAny])
def add_latest_info(request):
    username = request.data.get('username')

    print("Request Data:", request.data)

    if not username:
        return Response({"error": "Username is required"}, status=400)

    data = request.data.copy()  # Make mutable copy if needed
    serializer = LatestSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# post LatestInfo

# get LatestInfo

@api_view(['GET'])
@permission_classes([AllowAny])
def get_latest_info(request):
    username = request.query_params.get('username')

    if not username:
        return Response({"error": "Username is required"}, status=400)

    latest_info = LatestInfo.objects.filter(username=username).order_by('-id')
    count = latest_info.count()

    serializer = LatestSerializer(latest_info, many=True)
    return Response({
        'data': serializer.data,
        'count': count
    })


# get LatestInfo


# get FooterInfo

@api_view(['GET'])
@permission_classes([AllowAny])
def get_footer_info(request):
    try:
        username = request.query_params.get('username')

        if not username:
            return Response({'error': 'Username is required'}, status=400)

        footer_info = FooterInfo.objects.filter(username=username)
        serializer = FooterSerializer(footer_info, many=True)
        return Response(serializer.data, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


# get FooterInfo


# post FooterInfo
@api_view(['POST'])
@permission_classes([AllowAny])
def add_footer_info(request):
    username = request.data.get('username')

    if not username:
        return Response({"error": "Username is required"}, status=400)

    try:
        footer_info = FooterInfo.objects.get(username=username)

        # ✅ Update existing footer info
        data = request.data.copy()
        serializer = FooterSerializer(footer_info, data=data, partial=True)

    except FooterInfo.DoesNotExist:
        # ✅ Create new footer info
        serializer = FooterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)


# post FooterInfo


@api_view(['GET'])
@permission_classes([AllowAny])
def get_projects_info(request):
    username = request.query_params.get('username')

    if not username:
        return Response({"error": "Username is required"}, status=400)

    try:
        # projects_info = ProjectsInfo.objects.get(username=username)
        # serializer = ProjectsSerializer(projects_info)
        # count = ProjectsInfo.objects.count()
        projects_info = ProjectsInfo.objects.filter(username=username)  # ✅ change here
        serializer = ProjectsSerializer(projects_info, many=True)  # ✅ and here
        count = projects_info.count()
        return Response({
                'data': serializer.data,
                'count': count
            })
    except ProjectsInfo.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# get HomeInfo


# post ProjectsInfo

@api_view(['POST'])
@permission_classes([AllowAny])
def add_projects_info(request):
    username = request.data.get('username')

    print("Request Data:", request.data)

    if not username:
        return Response({"error": "Username is required"}, status=400)

    data = request.data.copy()  # Make mutable copy if needed
    serializer = ProjectsSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# post ProjectsInfo


# projectsDel

# @api_view(['DELETE'])
# def delete_projects_info(request, pk):
#     try:
#         project = ProjectsInfo.objects.get(pk=pk)
#         project.delete()
#         return Response(status=204)
#     except LatestInfo.DoesNotExist:
#         return Response({'error': 'Project not found'}, status=404)

# projectsDel

# get LatestInfo

# @api_view(['GET'])
# def get_latest_info(request):
#     latest_info = LatestInfo.objects.all()
#     count = LatestInfo.objects.count()
#     serializer = LatestSerializer(latest_info, many=True)
#     return Response({
#         'data': serializer.data,
#         'count': count
#     })


# get LatestInfo


# latestDel

# @api_view(['DELETE'])
# def delete_latest_info(request, pk):
#     try:
#         project = LatestInfo.objects.get(pk=pk)
#         project.delete()
#         return Response(status=204)
#     except LatestInfo.DoesNotExist:
#         return Response({'error': 'Project not found'}, status=404)


# latestDel



