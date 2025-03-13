from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, RoundViewSet, GameViewSet

router = DefaultRouter()
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'games', GameViewSet, basename='game')
router.register(r'rounds', RoundViewSet, basename='round')

urlpatterns = [
    path('', include(router.urls)),
]
