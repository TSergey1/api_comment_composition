from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet,
                    CommentViewSet,
                    GenreViewSet,
                    GetTokenView,
                    RegistrationUserView,
                    ReviewViewSet,
                    TitleViewSet,
                    UserViewSet)


router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'users', UserViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urlpatterns = [
    path('signup/', RegistrationUserView.as_view(),
         name='registration_user'),
    path('token/', GetTokenView.as_view(), name='get_token'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include((auth_urlpatterns, 'auth'))),
]
