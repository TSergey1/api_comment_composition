from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class RegistrationUserSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя"""

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Не допустимое имя')
        return value

    class Meta:
        model = User
        fields = ('email', 'username')

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
    """Сериализатор получения токена"""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
