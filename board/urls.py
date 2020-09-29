from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include

from rest_framework.routers import DefaultRouter # class 를 경로 지정하기 위해서

from . import views

router = DefaultRouter(trailing_slash=False) #view에 있는 함수(클래스를 가져오기 위해서는 router 사용)
router.register('board', views.BoardViewset)

urlpatterns = [
    path('', include(router.urls)),
]