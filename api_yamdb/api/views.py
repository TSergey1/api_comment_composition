from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.serializers import (GetTokenSerializer,
                             UserCreateSerializer,
                             UserSerializerForAdmin,
                             UserSerializerForAuther)
from api.permissions import IsAdmin

User = get_user_model()


class RegistrationUserView(APIView):
    """Вьюсет для создания обьектов класса User."""
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        username = request.data.get('username')
        send_mail(
            subject='Код регистрации YaMDb',
            message=f'username: {username}, '
                    f'confirmation_code: {confirmation_code}',
            from_email='aaa@yamdb.com',
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    """Вьюсет для создания обьектов класса User."""
    def post(self, request):
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
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status.HTTP_200_OK)
        return Response({"message": "Неверный код подтверждения."},
                        status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet пользователей."""
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializerForAdmin
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=['get', 'patch'],
            detail=False,
            url_path='me',
            permission_classes=(IsAuthenticated,),
            serializer_class=UserSerializerForAuther)
    def me(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
