from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Не допустимое имя')
        return value

    class Meta:
        model = User
        fields = ('email', 'username')

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username')
            )
        ]

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializerForAdmin(serializers.ModelSerializer):
    """Сериализатор пользователей User для адимна"""

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')


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
