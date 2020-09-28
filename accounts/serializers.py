from rest_framework import serializers
from .models import *
# from allauth.account.adapter import get_adapter
# from allauth.account.utils import setup_user_email

from rest_auth.registration.serializers import RegisterSerializer

# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver


class ProfileSerializer(RegisterSerializer): #RegisterSerializer를 상속받아서 수정하기 즉 오버라이팅 해서 Phone이라는 필드와 Credits라는 필드를 추가했음!
    nickname = serializers.CharField(
        required=True,
        max_length=13,
    )

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        return data_dict