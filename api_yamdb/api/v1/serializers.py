from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb.settings import CONST
from .core import (BaseUserSerializer,
                   BaseUserValidators)
from reviews.models import (Category,
                            Comment,
                            Genre,
                            Review,
                            Title)


User = get_user_model()


class UserCreateSerializer(serializers.Serializer, BaseUserValidators):
    """Сериализатор регистрации пользователя."""

    username_validator = UnicodeUsernameValidator()

    username = serializers.CharField(
        max_length=CONST['MAX_LENGTH_USERNAME'],
        validators=[username_validator],
        required=True,
    )

    email = serializers.EmailField(
        max_length=CONST['MAX_LENGTH_EMAIL'],
        required=True,
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user = User.objects.filter(username=username, email=email)
        if not user.exists():
            if User.objects.filter(username=username):
                raise serializers.ValidationError(
                    'Пользователь с таким username уже существует'
                )
            if User.objects.filter(email=email):
                raise serializers.ValidationError(
                    'Пользователь с таким email уже существует'
                )
        return data


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор получения токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializerForAdmin(serializers.ModelSerializer,
                             BaseUserValidators,
                             BaseUserSerializer
                             ):
    """Сериализатор пользователей User для адимна."""
    pass


class UserSerializerForAuther(serializers.ModelSerializer, BaseUserSerializer):
    """Сериализатор пользователей User для автора."""

    class Meta(BaseUserSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений (кроме запросов 'list', 'retrieve')."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class ReadTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений (только запросов 'list', 'retrieve')."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )


class ReviewSerialaizer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, validated_data):
        """Проверка на уникальность отзыва."""

        if self.context.get('request').method != 'POST':
            return validated_data
        pk = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=pk)
        current_review = Review.objects.filter(
            title=title,
            author=self.context.get('request').user,
        )
        if current_review.exists():
            raise serializers.ValidationError(
                'Вы можете добавить только один отзыв к произведению!'
            )
        return validated_data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
