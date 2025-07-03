from rest_framework import serializers
from .models import HomeInfo, FooterInfo, ProjectsInfo, LatestInfo
from .models import AboutInfo


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


class LatestSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = LatestInfo
        fields = '__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsInfo
        fields = '__all__'
