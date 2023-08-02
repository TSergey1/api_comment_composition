from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Review, Title

User = get_user_model()


class UserCreateSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя."""
    username_validator = UnicodeUsernameValidator()

    username = serializers.CharField(
        max_length=150,
        validators=[username_validator],
        required=True,
    )

    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                'Использовать имя me запрещено.'
            )
        return value

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


class UserSerializerForAdmin(serializers.ModelSerializer):
    """Сериализатор пользователей User для адимна."""

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                'Использовать имя me запрещено.'
            )
        return value


class UserSerializerForAuther(serializers.ModelSerializer):
    """Сериализатор пользователей User для автора."""

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        read_only_fields = ('role',)


class ReviewSerialaizer(serializers.ModelSerializer):
    """Преобразование данных в формат Python для отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, validated_data):
        """Проверка на уникальность отзыва."""

        if self.context['request'].method != 'POST':
            return validated_data
        pk = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=pk)
        current_review = Review.objects.filter(
            title=title,
            author=self.context['request'].user,
        )
        if current_review.exists():
            raise serializers.ValidationError(
                'Вы можете добавить только один отзыв к произведению!'
            )
        return validated_data


class CommentSerializer(serializers.ModelSerializer):
    """Преобразование данных в формат Python для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
