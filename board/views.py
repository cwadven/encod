from django.shortcuts import render

from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import permissions

# Create your views here.
class BoardViewset(viewsets.ModelViewSet):
    queryset = Board.objects.all() #id만큼 가져오기
    serializer_class = BoardSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly)