from rest_framework import serializers
from .models import Experience, UserDetail
from django.contrib.auth.models import User


class ExperienceSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Experience.objects.create(**validated_data)

    class Meta:
        model = Experience
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return UserDetail.objects.create(**validated_data)

    class Meta:
        model = UserDetail
        fields = '__all__'
