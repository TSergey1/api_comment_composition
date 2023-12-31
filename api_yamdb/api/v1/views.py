from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .filters import TitleFilters
from .mixins import ListCreateDestroyMixins
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          GenreSerializer,
                          GetTokenSerializer,
                          ReadTitleSerializer,
                          ReviewSerialaizer,
                          TitleSerializer,
                          UserCreateSerializer,
                          UserSerializerForAdmin,
                          UserSerializerForAuther)
from .permissions import (IsAdmin,
                          IsAdminOrReadOnly,
                          IsAuthorOrAdminOrModeratOrReadOnly,)
from reviews.models import (Category,
                            Genre,
                            Review,
                            Title)

User = get_user_model()


class RegistrationUserView(APIView):
    """Вьюсет для создания обьектов класса User."""

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user, _ = User.objects.get_or_create(**serializer.validated_data)
            confirmation_code = default_token_generator.make_token(user)
            username = request.data.get('username')
            send_mail(
                subject='Код регистрации YaMDb',
                message=f'username: {username}, '
                        f'confirmation_code: {confirmation_code}',
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):
    """Вьюсет для получения токена"""

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        if default_token_generator.check_token(
            user,
            serializer.validated_data.get('confirmation_code')
        ):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status.HTTP_200_OK)
        return Response({"message": "Неверный код подтверждения."},
                        status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet пользователей."""

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializerForAdmin
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=['get', 'patch'],
            detail=False,
            url_path='me',
            permission_classes=(IsAuthenticated,),
            serializer_class=UserSerializerForAuther)
    def me(self, request):
        user = request.user
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyMixins):
    """Вьюсет для обьектов класса Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyMixins):
    """Вьюсет для обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов класса Title."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('genre',)
    filterset_class = TitleFilters
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс представлений для отзывов к произведениям."""

    serializer_class = ReviewSerialaizer
    permission_classes = (IsAuthorOrAdminOrModeratOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """Вернет кверисет отзывов для списочных и детальных представлений."""
        return Title.objects.get(
            pk=self.kwargs.get('title_id')
        ).reviews.all()

    def perform_create(self, serializer):
        """Создание отзыва, с проверкой на уникальнось в сериализаторе."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Класс представлений для комментариев к отзывам."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModeratOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"),
                                   title=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
