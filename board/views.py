from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsSuperUser
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Count, Case, When, BooleanField

# Create your views here.
class BoardViewset(viewsets.ModelViewSet):
    # queryset = Board.objects.all() #id만큼 가져오기
    serializer_class = BoardSerializer
    #관리자만 작성 가능
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsSuperUser)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend] #DjangoFilterBackend 사용
    filterset_fields = ['ended', ]

    # 내가 지금 했는지 판별 get_queryset을 modelviewset에서 이용하려면 url에 3번째 파라미터에 '이름'을 넣어줘야 한다
    # 직접 받는 쿼리를 self의 매게변수를 이용하여 voted라는 GET 정보를 받으면  내꺼 기준으로 필터링 됨!
    def get_queryset(self):
        user = self.request.user
        if self.request.GET.get('voted'):
            try:
                if bool(int(self.request.GET.get('voted'))):
                    return Board.objects.filter(voter__in=[user.id])
                else:
                    return Board.objects.exclude(voter__in=[user.id])
            except:
                if bool(self.request.GET.get('voted').lower() == 'true'):
                    return Board.objects.filter(voter__in=[user.id])
                else:
                    return Board.objects.exclude(voter__in=[user.id])
        else:
            return Board.objects.all()
        # .annotate(q_count=Count('voter')).order_by("-q_count") 추후에 추가

    def perform_create(self, serializer): #자동으로 자기 자신 author에 저장 되도록
        serializer.save(author=self.request.user)

    def perform_update(self, serializer): #자동으로 자기 자신 author에 저장 되도록
        serializer.save(author=self.request.user)

class HotBoardView(APIView):
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsSuperUser)

    def get(self, request):
        board = Board.objects.filter(ended=False).annotate(q_count=Count('voter')).order_by("-q_count")[0]

        serializer = BoardSerializer(
            board, context={"request": request}
        )

        data=serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

class VoteBoardView(APIView):
    # queryset = VoteBoard.objects.all()
    serializer_class = VoteBoardSerializer
    # 관리자만이 쓸수 있도록 설정
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsSuperUser)

    def get(self, request, format=None):
        all_Board = VoteBoard.objects.all()
        
        # context 안에 get으로 가져온 request를 뿌려줘서 serializers에서 사용할 수 있도록
        serializer = ShowVoteBoardSerializer(
            all_Board, many=True, context={"request": request}
        )

        return Response(data=serializer.data)

    def post(self, request, format=None):
        #context={"request": request}가 있어야 image의 전체 줄이 나온다
        serializer = VoteBoardSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"detail":"boardid missing"} , status=status.HTTP_400_BAD_REQUEST)

class VoteBoardDetailView(APIView):
    serializer_class = VoteBoardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # 작성자만 처리 가능할 수 있도록 하는 함수 따로 설정 board가 작성자인지 판단후 작성자면 board 출력 아니면 None
    def find_own_board(self, item_id, author):
        try:
            board = VoteBoard.objects.get(id=item_id)
            if board.boardid.author == author:
                return board
            else:
                return None
        except:
            return False

    def get(self, request, item_id, format=None):
        try:
            board = VoteBoard.objects.get(id=item_id)
        except:
            return Response(data={"detail":"no vote article"}, status=status.HTTP_404_NOT_FOUND)
        
        # serializer = VoteBoardSerializer(board, context={"request": request})
        if request.user in board.voter.all():
            voted = True
        else:
            voted = False

        serializer = ShowVoteBoardSerializer(
            board, context={"request": request}
        )

        data=serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    # 특정 게시글을 포스트 하면 add 가된다!
    def post(self, request, item_id, format=None):
        serializer = PostVoteBoardSerializer(data=request.data)
        try:
            board = VoteBoard.objects.get(id=item_id)
            if board.boardid.ended == False:
            # 만약 해당 voter에 있을 경우 한것이 있을 경우
                if request.user in board.voter.all():
                    board.voter.remove(request.user.id)
                    board.boardid.voter.remove(request.user.id)
                    voted = False
                # 만약 해당 voter에 없을 경우 참조하는 모든 것을 확인하고 있으면 지우고 없으면 그냥 넘어간다
                else:
                    for i in board.boardid.contents.all():
                        try:
                            i.voter.remove(request.user.id)
                            i.save()
                        except:
                            pass
                    board.voter.add(request.user)
                    board.boardid.voter.add(request.user)
                    voted = True
            else:
                return Response(data={"detail":"voted is ended"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(data={"detail":"no vote article"}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            # 직접 하나하나씩 넣었음

            serializer = ShowVoteBoardSerializer(
                board, context={"request": request}
            )

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 수정은 작성자만 수정 가능하게
    def put(self, request, item_id, format=None):
        try:
            board = self.find_own_board(item_id, request.user)
            if board == None:
                return Response(data={"detail":"not Authorized"}, status=status.HTTP_400_BAD_REQUEST)
            elif board == False:
                return Response(data={"detail":"no vote article"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(data={"detail":"no vote article"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShowVoteBoardSerializer(
            board, data=request.data, context={"request": request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id, format=None):
        # 작성자만 삭제가능
        try:
            board = self.find_own_board(item_id, request.user)
            if board == None:
                return Response(data={"detail":"not Authorized"}, status=status.HTTP_400_BAD_REQUEST)
            elif board == False:
                return Response(data={"detail":"no vote article"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(data={"detail":"no vote article"}, status=status.HTTP_404_NOT_FOUND)
        
        # 삭제되면 주제 투표게시글에 있는 voter도 삭제
        for i in board.voter.all():
            board.boardid.voter.remove(i)

        board.delete()
        # serializer_class = UpdateVoteBoardSerializer
        return Response(status=status.HTTP_204_NO_CONTENT)