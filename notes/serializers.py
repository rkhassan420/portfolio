from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import serializers
from .models import Note

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    # notes/serializers.py


class NoteSerializer(serializers.ModelSerializer):
        user = serializers.ReadOnlyField(source="user.username")

        class Meta:
            model = Note
            fields = ["id", "user", "title", "body",  "date"]

