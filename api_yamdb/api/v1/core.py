from django.contrib.auth import get_user_model

User = get_user_model()


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
