from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Player, Round, Game
from .serializers import PlayerSerializer, RoundSerializer, GameSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        game = Game.objects.get(id=data['game'])

        if game.is_finished:
            return Response(
                {"error": "El juego ya ha finalizado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RoundSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            game.refresh_from_db()
            if game.is_finished:
                return Response({
                    "message": f"El juego ha terminado. ¡Ganador: {game.winner}!",
                    "game": GameSerializer(game).data
                })
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
