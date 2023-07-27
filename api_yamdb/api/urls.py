from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import get_token, RegistrationUserView


router = DefaultRouter()

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationUserView.as_view(),
         name='registration_user'),
    path('v1/auth/token/', get_token, name='get_token'),
]
