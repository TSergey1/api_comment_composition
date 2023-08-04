from django.contrib.auth import get_user_model
from rest_framework import serializers

from api_yamdb.settings import CONST

User = get_user_model()


class BaseUserValidators:
    """Базовый класс валидаторов User."""
    def validate_username(self, value):
        if value.lower() == CONST['FORBIDDEN_USERNAME']:
            raise serializers.ValidationError(
                'Использовать имя me запрещено.'
            )
        return value


class BaseUserSerializer:
    """Базовый класс Serializer User."""

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
