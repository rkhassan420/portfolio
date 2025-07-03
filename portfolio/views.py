from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
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



# get HomeInfo

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_home_info(request):
#     home_info = HomeInfo.objects.all()
#     serializer = HomeSerializer(home_info, many=True)
#     return Response(serializer.data)

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



# post HomeInfo

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def add_home_info(request):
#     try:
#         home_info = HomeInfo.objects.first()
#
#         if home_info:
#             data = request.data.copy()
#
#
#             if not request.FILES.get('image'):
#                 data['image'] = home_info.image
#             if not request.FILES.get('cv'):
#                 data['cv'] = home_info.cv
#
#             serializer = HomeSerializer(home_info, data=data)
#         else:
#             serializer = HomeSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)


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
        if not request.FILES.get('image'):
            data['image'] = home_info.image  # Existing image instance
        if not request.FILES.get('cv'):
            data['cv'] = home_info.cv  # Existing cv instance

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
def get_about_info(request):
    about_info = AboutInfo.objects.all()
    serializer = AboutSerializer(about_info, many=True)
    return Response(serializer.data)


# get AboutInfo


# post AboutInfo

@api_view(['POST'])
def add_about_info(request):
    try:
        # Get the existing object (since only one exists)
        about_info = AboutInfo.objects.first()

        if about_info:
            # Use the serializer but only update fields that are not empty
            data = request.data.copy()

            # These are file fields — check if they're empty
            if not request.FILES.get('image'):
                data['image'] = about_info.image  # keep existing

            serializer = AboutSerializer(about_info, data=data)
        else:
            serializer = AboutSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


# post AboutInfo


# get FooterInfo

@api_view(['GET'])
def get_footer_info(request):
    footer_info = FooterInfo.objects.all()
    serializer = FooterSerializer(footer_info, many=True)
    return Response(serializer.data)


# get FooterInfo


# post FooterInfo

@api_view(['POST'])
def add_footer_info(request):
    try:
        # Get the existing FooterInfo object (if any)
        footer_info = FooterInfo.objects.first()

        if footer_info:
            # Update the existing object with new data
            serializer = FooterSerializer(footer_info, data=request.data)
        else:
            # Create a new object
            serializer = FooterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


# post FooterInfo


# get ProjectsInfo

@api_view(['GET'])
def get_projects_info(request):
    projects_info = ProjectsInfo.objects.all()
    count = ProjectsInfo.objects.count()
    serializer = ProjectsSerializer(projects_info, many=True)
    return Response({
        'data': serializer.data,
        'count': count
    })



# get ProjectsInfo


# post ProjectsInfo

@api_view(['POST'])
def add_projects_info(request):
    projects_info = AboutInfo.objects.all()
    serializer = ProjectsSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# post ProjectsInfo



# get LatestInfo

@api_view(['GET'])
def get_latest_info(request):
    latest_info = LatestInfo.objects.all()
    count = LatestInfo.objects.count()
    serializer = LatestSerializer(latest_info, many=True)
    return Response({
        'data': serializer.data,
        'count': count
    })


# get LatestInfo


# post LatestInfo

@api_view(['POST'])
def add_latest_info(request):
    latest_info = LatestInfo.objects.all()
    serializer = LatestSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# post LatestInfo


# latestDel

@api_view(['DELETE'])
def delete_latest_info(request, pk):
    try:
        project = LatestInfo.objects.get(pk=pk)
        project.delete()
        return Response(status=204)
    except LatestInfo.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)

# latestDel



# projectsDel

@api_view(['DELETE'])
def delete_projects_info(request, pk):
    try:
        project = ProjectsInfo.objects.get(pk=pk)
        project.delete()
        return Response(status=204)
    except LatestInfo.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)

# projectsDel


