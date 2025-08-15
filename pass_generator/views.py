from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .utils import generate_password, check_strength


@api_view(['POST'])
@permission_classes([AllowAny])
def password_generator(request):
    try:
        length = int(request.data.get("length", 12))
        use_upper = request.data.get("use_upper", True)
        use_lower = request.data.get("use_lower", True)
        use_digits = request.data.get("use_digits", True)
        use_symbols = request.data.get("use_symbols", True)

        password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        return Response({
            "password": password,
            "strength": check_strength(password)
        })

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_strength(request):
    password = request.data.get("password", "")
    if not password:
        return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "password": password,
        "strength": check_strength(password)
    })
