from rest_framework.mixins import (ListModelMixin,
                                   CreateModelMixin,
                                   DestroyModelMixin)
from rest_framework.viewsets import GenericViewSet


class ListCreateDestroyMixins(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """Базовый сериализатор для произведений."""

    pass
