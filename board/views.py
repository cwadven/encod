from django.shortcuts import render

from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly

# Create your views here.
class BoardViewset(viewsets.ModelViewSet):
    queryset = Board.objects.all() #id만큼 가져오기
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer): #자동으로 자기 자신 author에 저장 되도록
        serializer.save(author=self.request.user)

    def perform_update(self, serializer): #자동으로 자기 자신 author에 저장 되도록
        serializer.save(author=self.request.user)