from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator


User = get_user_model()


class UserCreateSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя."""

    username = serializers.CharField(
        max_length=150,
        validators=(UnicodeUsernameValidator,),
        required=True,
    )

    email = serializers.CharField(
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
                    'ользователь с таким username существует'
                )
            if User.objects.filter(email=email):
                raise serializers.ValidationError(
                    'Пользователь с таким email существует'
                )
        return data


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializerForAdmin(serializers.ModelSerializer):
    """Сериализатор пользователей User для адимна."""

    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')

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
