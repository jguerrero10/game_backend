"""
Service class for game-related operations.
"""

from typing import Optional


class GameService:
    """Service class for game-related operations."""

    @staticmethod
    def determine_round_winner(player_1_move: str, player_2_move: str, game: "Game") -> Optional["Player"]:
        """Determine the winner of a round based on the players' moves."""
        if player_1_move == player_2_move:
            return None

        moves = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper',
        }

        return game.player_1 if moves[player_1_move] == player_2_move else game.player_2

    @staticmethod
    def update_game_score(round_instance: "Round"):
        """Update the game score based on the round winner."""
        game = round_instance.game
        if game.is_finished:
            return

        if round_instance.winner == game.player_1:
            game.player_1_wins += 1
        elif round_instance.winner == game.player_2:
            game.player_2_wins += 1

        if game.player_1_wins >= 3 or game.player_2_wins >= 3:
            game.is_finished = True
            game.winner = game.player_1 if game.player_1_wins >= 3 else game.player_2

        game.save()
