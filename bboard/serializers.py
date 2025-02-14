from rest_framework import serializers

from .models import Rubric, Bb


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        # __fields__ = '__all__'
        fields = ('id', 'name')
