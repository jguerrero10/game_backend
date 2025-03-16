"""URL configuration for the Game app."""

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import GameViewSet, PlayerViewSet, RoundViewSet

router = DefaultRouter()
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'games', GameViewSet, basename='game')
router.register(r'rounds', RoundViewSet, basename='round')

urlpatterns = [
    path('', include(router.urls)),
]
