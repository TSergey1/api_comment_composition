from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrAdminOrModeratOrReadOnly
from api.serializers import CommentSerializer, ReviewSerialaizer
from reviews.models import Comment, Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс представлений для отзывов к произведениям."""

    serializer_class = ReviewSerialaizer
    permission_classes = (IsAuthorOrAdminOrModeratOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Получение списка/одного комментария, в зависимости от запроса."""

        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        """Создание отзыва, с проверкой на уникальнось в сериализаторе."""

        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Класс представлений для комментариев к отзывам."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModeratOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Получение списка/одного комментария, в зависимости от запроса."""

        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        """Создание нового комментария, без проверок на уникальность."""

        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
