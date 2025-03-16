"""Views for the game app."""
from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Game, Player, Round
from .serializers import GameSerializer, PlayerSerializer, RoundSerializer, TopPlayerSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """API endpoint that allows players to be viewed or edited."""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @action(detail=False, methods=['get'])
    def top_winners(self, request):
        """Return the top 5 players with the most wins."""
        top_players = (
            Player.objects
            .values('name')
            .annotate(total_wins=Count('games_won'))
            .order_by('-total_wins')[:5]
        )
        serializer = TopPlayerSerializer(top_players, many=True)
        return Response(serializer.data)


class GameViewSet(viewsets.ModelViewSet):
    """API endpoint that allows games to be viewed or edited"""

    queryset = Game.objects.all()
    serializer_class = GameSerializer

class RoundViewSet(viewsets.ModelViewSet):
    """API endpoint that allows rounds to be viewed or edited."""

    queryset = Round.objects.all()
    serializer_class = RoundSerializer

    def create(self, request, *args, **kwargs):
        """Create a new round and check if the game has finished."""
        data = request.data
        try:
            game = Game.objects.get(id=data['game'])
        except Game.DoesNotExist:
            return Response({"error": "El juego no existe."}, status=status.HTTP_400_BAD_REQUEST)

        if game.is_finished:
            return Response({"error": "El juego ya ha finalizado."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RoundSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            game.refresh_from_db()

            if game.is_finished:
                return Response(
                    {"message": f"El juego ha terminado. ¡Ganador: {game.winner}!", "game": GameSerializer(game).data},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
