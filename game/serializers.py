"""Serializers for the Game app."""

from rest_framework import serializers

from .models import Game, Player, Round


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for the Player model."""

    class Meta:
        """Metadata class for the PlayerSerializer"""

        model = Player
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    """Serializer for the Game model."""

    class Meta:
        """Metadata class for the GameSerializer"""

        model = Game
        fields = '__all__'



class RoundSerializer(serializers.ModelSerializer):
    """Serializer for the Round model."""
    player_1_move = serializers.ChoiceField(choices=['rock', 'paper', 'scissors'], required=True)
    player_2_move = serializers.ChoiceField(choices=['rock', 'paper', 'scissors'], required=True)
    winner_name = serializers.CharField(read_only=True, source='winner.name', null=True)

    class Meta:
        """Metadata class for the RoundSerializer"""
        model = Round
        fields = '__all__'
