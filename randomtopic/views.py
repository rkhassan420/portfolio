import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import TopicAssignmentSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def assign_topics(request):
    serializer = TopicAssignmentSerializer(data=request.data)
    if serializer.is_valid():
        students = serializer.validated_data['students']
        topics = serializer.validated_data['topics']

        if len(students) > len(topics):
            return Response(
                {"error": "Not enough topics for all students"},
                status=status.HTTP_400_BAD_REQUEST
            )

        random.shuffle(topics)
        assignments = {}
        for i, student in enumerate(students):
            assignments[student] = topics[i]

        return Response({"assignments": assignments})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
