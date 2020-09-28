from .models import *
from rest_framework import serializers

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        models = Board
        field = ('__all__')