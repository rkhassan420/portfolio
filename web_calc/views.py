from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from .serializers import AgeSerializer

@method_decorator(csrf_exempt, name='dispatch')
class AgeCalculatorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AgeSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
