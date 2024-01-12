from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    access_token = serializers.CharField()
