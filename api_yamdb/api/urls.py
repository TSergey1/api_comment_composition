from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet
)


router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
