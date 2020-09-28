from .models import *
from accounts.models import Profile
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer): #author 안에 있는 정보를 가져오기 위해서 TBoard랑 author로 관계가 있는 UserSerializer를 통해서 새로 만듦  
    class Meta:
        model = Profile
        fields = ("id", "username", "nickname",)  

class BoardSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Board
        fields = ('id', 'author', 'title', 'body', 'created_at', 'updated_at')