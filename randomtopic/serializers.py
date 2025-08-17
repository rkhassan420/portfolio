from rest_framework import serializers

class TopicAssignmentSerializer(serializers.Serializer):
    students = serializers.ListField(
        child=serializers.CharField(), allow_empty=False
    )
    topics = serializers.ListField(
        child=serializers.CharField(), allow_empty=False
    )
