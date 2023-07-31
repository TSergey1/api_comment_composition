from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrModeratOrReadOnly,
    IsAdmin
)

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)

from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'slug')
    # permission_classes = (
    #     IsAdminOrReadOnly,
    #     permissions.IsAuthenticatedOrReadOnly,
    # )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'slug')
    # permission_classes = (
    #     IsAdminOrReadOnly,
    #     permissions.IsAuthenticatedOrReadOnly,
    # )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
