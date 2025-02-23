from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # __fields__ = '__all__'
        fields = ("id", "username", "email")



