from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LoginView,
    MeView,
    UsuarioViewSet,
    PerfilViewSet
)


router = DefaultRouter()

router.register(
    'usuarios',
    UsuarioViewSet
)

router.register(
    'perfis',
    PerfilViewSet
)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
]