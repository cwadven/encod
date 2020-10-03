from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('user', views._UpdateView.as_view(), name='_update'),
    # path('user/delete', views._DeleteUser.as_view(), name='_delete'),
]