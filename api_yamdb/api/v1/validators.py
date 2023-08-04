from rest_framework import serializers

from api_yamdb.settings import CONST


class BaseValidate():
    """Общий класс валидации."""

    def validate_username(self, value):
        if value.lower() == CONST['FORBIDDEN_USERNAME']:
            raise serializers.ValidationError(
                'Использовать имя me запрещено.'
            )
        return value
