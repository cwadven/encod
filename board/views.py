from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsSuperUser
from django.db.models import Count

# Create your views here.
class BoardViewset(viewsets.ModelViewSet):
    queryset = Board.objects.all() #id만큼 가져오기
    serializer_class = BoardSerializer
    #관리자만 작성 가능
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsSuperUser)

    def perform_create(self, serializer): #자동으로 자기 자신 author에 저장 되도록
        serializer.save(author=self.request.user)

    def perform_update(self, serializer): #자동으로 자기 자신 author에 저장 되도록
        serializer.save(author=self.request.user)

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
        serializer = VoteBoardSerializer(data=request.data)
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