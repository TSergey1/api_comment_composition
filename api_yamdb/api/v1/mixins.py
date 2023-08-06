from rest_framework import filters
from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin,
                                   DestroyModelMixin)
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrReadOnly


class ListCreateDestroyMixins(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """Базовый сериализатор для произведений."""

    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
