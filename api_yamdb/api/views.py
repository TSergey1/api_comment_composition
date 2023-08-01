from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorOrAdminOrModeratOrReadOnly
from api.serializers import CommentSerializer, ReviewSerialaizer
from reviews.models import Comment, Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerialaizer
    permission_classes = (IsAuthorOrAdminOrModeratOrReadOnly,)
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        return get_list_or_404(Review, title=self.kwargs['title_id'])

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModeratOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return get_list_or_404(Comment, review=self.kwargs['review_id'])

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
