from rest_framework import serializers
from .models import Calls
from django.contrib.auth.models import User

class CallsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Calls.objects.create(**validated_data)

    class Meta:
        model = Calls
        fields = '__all__'
