from .models import *
from rest_framework import serializers

class BoardSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Board
        fields = ('id', 'author_username', 'title', 'body', 'created_at', 'updated_at')