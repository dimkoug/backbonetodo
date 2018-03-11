from django.urls import path, include
from rest_framework import routers
from .viewsets import UserViewSet, TodoViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register('users', UserViewSet)
router.register('todos', TodoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
