from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from api.serializers import GetTokenSerializer, RegistrationUserSerializer

User = get_user_model()


class RegistrationUserView(APIView):
    """Вьюсет для создания обьектов класса User."""
    def post(self, request, format=None):
        serializer = RegistrationUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user, _ = User.objects.get_or_create(**serializer.validated_data)
            confirmation_code = default_token_generator.make_token(user)
            username = request.data.get('username')
            username
            send_mail(
                subject='Код регистрации YaMDb',
                message=f'username: {username}, '
                        f'confirmation_code: {confirmation_code}',
                from_email='aaa@yamdb.com',
                recipient_list=[user.email],
                fail_silently=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получение токена"""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        token = RefreshToken.for_user(user)
        return Response({"token": str(token)}, status.HTTP_200_OK)

    return Response({"message": "Неверный код подтверждения."},
                    status.HTTP_400_BAD_REQUEST)
