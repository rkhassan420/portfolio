from rest_framework import serializers
from .models import HomeInfo, FooterInfo, ProjectsInfo, AboutInfo, OTPVerification


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeInfo
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutInfo
        fields = '__all__'


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterInfo
        fields = '__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    image = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = ProjectsInfo
        fields = '__all__'


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = ['email', 'otp', 'is_verified']
