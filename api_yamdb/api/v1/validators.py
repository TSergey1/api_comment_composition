from rest_framework import serializers


class BaseValidate():
    """Общий класс валидации."""

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                'Использовать имя me запрещено.'
            )
        return value
