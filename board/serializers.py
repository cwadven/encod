from .models import *
from rest_framework import serializers

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('__all__')