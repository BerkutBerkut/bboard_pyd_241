
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Rubric, Bb


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        # __fields__ = '__all__'
        fields = ('id', 'name')


class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        # __fields__ = '__all__'
        fields = ("id", "title", "content", "price")
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'