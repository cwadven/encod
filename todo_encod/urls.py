from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
import board.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    #게시글 접근
    path('', include('board.urls')),
]
