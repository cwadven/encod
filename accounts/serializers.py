from rest_framework import serializers
from .models import *

from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.validators import UniqueValidator

class ProfileUpdateSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(
        required=True,
        min_length=3,
        max_length=13,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    class Meta:
        model = Profile
        fields = ("nickname",)  
    

class ProfileSerializer(RegisterSerializer): #RegisterSerializer를 상속받아서 수정하기 즉 오버라이팅 해서 Phone이라는 필드와 Credits라는 필드를 추가했음!
    nickname = serializers.CharField(
        required=True,
        min_length=3,
        max_length=13,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        return data_dict