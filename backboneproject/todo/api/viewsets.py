from rest_framework import viewsets, authentication, filters
from django_filters import rest_framework as django_filters
from django.contrib.auth import get_user_model

from ..models import Todo


from .serializers import UserSerializer, TodoSerializer
from .permissions import IsOwnerOrReadOnly, ListRouteIsAuthenticated
User = get_user_model()


class DefaultsMixin(object):
    """Default settings for view authentication, permissions,
    filtering and pagination."""
    authentication_classes = (
        authentication.TokenAuthentication,
    )
    permission_classes = (
        IsOwnerOrReadOnly,
        ListRouteIsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    permission_classes = (
        ListRouteIsAuthenticated,
    )


class TodoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Todo.objects.order_by('-created')
    serializer_class = TodoSerializer
    search_fields = ('title',)
    ordering_fields = ('title', 'created')

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        return False
