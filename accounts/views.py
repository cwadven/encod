from .models import *
from .serializers import *
import json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from django.core import serializers


#views는 받은 값 처리하기 serializer는 forms 같은 규격
class _UpdateView(APIView):
    #로그인 한 사람만 접근 가능
    serializer_class = ProfileUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    #수정하기
    def put(self, request):
        #r값을 request.data.get으로 가져오기
        profile_information = Profile.objects.get(username=self.request.user)
        nickname = request.data.get("nickname")
        data = {'nickname': nickname}

        #만약에 양식에 맞으면!
        serializer = ProfileUpdateSerializer(data=data)
        if serializer.is_valid():
            #닉네임 수정하기
            profile_information.nickname = serializer.data['nickname']
            profile_information.save()
            data = serializers.serialize('json', [profile_information,], fields=["username", "email", "nickname"])
            data = json.loads(data)
            #수정 완료하면 수정된 정보 보여주기
            return Response(data[0]["fields"], status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            profile = Profile.objects.get(username=self.request.user)
            profile.delete()
            return Response(data={"detail":"user deleted"} , status=status.HTTP_202_ACCEPTED)
        except:
            return Response(data={"detail":"something get wrong"} , status=status.HTTP_400_BAD_REQUEST)