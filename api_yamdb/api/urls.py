from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (CommentViewSet,
                       GetTokenView,
                       RegistrationUserView,
                       ReviewViewSet,
                       UserViewSet)


router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationUserView.as_view(),
         name='registration_user'),
    path('v1/auth/token/', GetTokenView.as_view(), name='get_token'),
]
