from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AgeSerializer

@csrf_protect
@permission_classes([AllowAny])
class AgeCalculatorView(APIView):
    def post(self, request):
        serializer = AgeSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


