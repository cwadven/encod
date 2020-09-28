from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
import board.urls

#jwt 토큰 사용
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    #게시글 접근
    path('', include('board.urls')),
    path('api/token/', obtain_jwt_token),
    path('api/token/verify/', verify_jwt_token),
    path('api/token/refresh/', refresh_jwt_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
