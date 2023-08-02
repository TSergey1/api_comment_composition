from django.db.models import Avg
from api.mixins import ListCreateDestroyViewSet
from rest_framework import filters, viewsets

from api.permissions import IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReadTitleSerializer
)

from reviews.models import Category, Genre, Title


class CategoryViewSet(ListCreateDestroyViewSet):
    """Вьюсет для обьектов класса Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет для обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов класса Title."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('genre',)
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadTitleSerializer
        return TitleSerializer
