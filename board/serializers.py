from .models import *
from accounts.models import Profile
from rest_framework import serializers
import json
from django.core import serializers as d_serializers
from django.db.models import Count

class UserSerializer(serializers.ModelSerializer): #author 안에 있는 정보를 가져오기 위해서 TBoard랑 author로 관계가 있는 UserSerializer를 통해서 새로 만듦  
    class Meta:
        model = Profile
        fields = ("id", "username", "nickname",)

class VoteBoardSerializer(serializers.ModelSerializer):
    voted = serializers.SerializerMethodField()

    # 총 투표자 새기
    voter_count = serializers.SerializerMethodField()

    # boardid = serializers.PrimaryKeyRelatedField(read_only=True)

    # put을 할때 꼭 필요없다 라고 말하기
    image = serializers.ImageField(required=False)
    title = serializers.CharField(required=False)

    class Meta:
        model = VoteBoard
        fields = ("id", "boardid", "title", "created_at", "updated_at", "voter_count", "voted", "image")

    # 내가 투표를 했는지 안했는지 확인
    def get_voted(self, obj):
        # 회원이 아닐 경우 False로
        try:
            if self.context.get('request').user in obj.voter.all():
                return True
            else:
                return False
        except:
            return False

    def get_voter_count(self, obj): 
        # 총 몇 명의 투표자가 있는지 확인하기 위해서
        return obj.voter.count()

class UpdateVoteBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteBoard
        fields = ("title", "image")

class PostVoteBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteBoard
        fields = ("voter",)

#BoardSerializer안에 넣기 위해서 사용
class ShowVoteBoardSerializer(serializers.ModelSerializer):
    #내가 투표를 했는지 않했는지
    voted = serializers.SerializerMethodField()

    # 총 투표자 새기
    voter_count = serializers.SerializerMethodField()

    boardid = serializers.PrimaryKeyRelatedField(read_only=True)

    # put을 할때 꼭 필요없다 라고 말하기
    image = serializers.ImageField(required=False)
    title = serializers.CharField(required=False)

    class Meta:
        model = VoteBoard
        fields = ("id", "boardid", "title", "created_at", "updated_at", "voter_count", "voted", "image")

    # 내가 투표를 했는지 안했는지 확인
    def get_voted(self, obj):
        # 회원이 아닐 경우 False로
        try:
            if self.context.get('request').user in obj.voter.all():
                return True
            else:
                return False
        except:
            return False

    def get_voter_count(self, obj): 
        # 총 몇 명의 투표자가 있는지 확인하기 위해서
        return obj.voter.count()

class BoardSerializer(serializers.ModelSerializer):
    # author = UserSerializer(read_only=True)
    
    # 총 투표자 새기
    voter_count = serializers.SerializerMethodField()

    # 이기고 있는거 보기
    winner_id = serializers.SerializerMethodField()

    title = serializers.CharField(required=False)

    ended = serializers.BooleanField(required=False)

    # 투표 게시판의 투표 할 것 정보 가져오기
    contents = ShowVoteBoardSerializer(read_only=True, many=True)

    voted = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ('id', 'title', 'voter_count', 'contents', 'winner_id', 'ended', 'voted', 'created_at', 'updated_at',)

    #obj는 Board의 objects 들이다
    def get_voter_count(self, obj): 
        # 총 몇 명의 투표자가 있는지 확인하기 위해서
        return obj.voter.all().count()

    # 이기고 있는 투표 찾기
    def get_winner_id(self, obj):
        qs = obj.contents.all().annotate(winner=Count('voter')).order_by("-winner")
        
        # winner의 수 중 max를 구하기 (동점일 경우가 있을 수 있으니!)
        _max = sorted(qs.values("winner"), key=lambda x: x['winner'], reverse=True)
        
        winner_id = list()

        try:
            for i in qs.filter(winner=_max[0]["winner"]):
                winner_id.append(i.id)
        except:
            pass
            
        return winner_id

    def get_voted(self, obj):
        # 회원이 아닐 경우 False로
        try:
            if self.context.get('request').user in obj.voter.all():
                return True
            else:
                return False
        except:
            return False