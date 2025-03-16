"""
Unit tests for the Game model.
"""

from django.test import TestCase
from game.models import Player, Game, Round
from game.service.game_service import GameService


class GameModelTestCase(TestCase):
    """Unit tests for the Game model."""

    def setUp(self):
        """Set up the test case with initial data."""
        self.player_1 = Player.objects.create(name="Player 1")
        self.player_2 = Player.objects.create(name="Player 2")
        self.game = Game.objects.create(player_1=self.player_1, player_2=self.player_2)

    def test_create_game(self):
        """Test creating a new game."""
        self.assertEqual(self.game.player_1, self.player_1)
        self.assertEqual(self.game.player_2, self.player_2)
        self.assertEqual(self.game.player_1_wins, 0)
        self.assertEqual(self.game.player_2_wins, 0)
        self.assertFalse(self.game.is_finished)
        self.assertIsNone(self.game.winner)

    def test_create_round(self):
        """Test creating a new round."""
        round_instance = Round.objects.create(game=self.game, player_1_move='rock', player_2_move='scissors')
        self.assertEqual(round_instance.game, self.game)
        self.assertEqual(round_instance.player_1_move, 'rock')
        self.assertEqual(round_instance.player_2_move, 'scissors')

    def test_round_with_no_moves(self):
        """Test the case where both players do not choose any move."""
        round_instance = Round.objects.create(
            game=self.game,
            player_1_move=None,
            player_2_move=None
        )
        self.assertIsNone(round_instance.winner)

    def test_determine_round_winner_tie(self):
        """Test determining the winner of a round when it's a tie."""
        winner = GameService.determine_round_winner('rock', 'rock', self.game)
        self.assertIsNone(winner)

    def test_update_game_score_when_game_is_finished(self):
        """Test updating the game score when the game is already finished."""
        self.game.player_1_wins = 3
        self.game.is_finished = True
        self.game.save()

        round_instance = Round.objects.create(
            game=self.game,
            player_1_move='rock',
            player_2_move='scissors',
            winner=self.player_1
        )

        GameService.update_game_score(round_instance)
        self.game.refresh_from_db()

        self.assertEqual(self.game.player_1_wins, 3)

    def test_round_winner_determined_during_save(self):
        """Test determining the round winner during the save method."""
        round_instance = Round.objects.create(
            game=self.game,
            player_1_move='rock',
            player_2_move='scissors',
            winner=None
        )

        round_instance.save()

        self.assertEqual(round_instance.winner, self.player_1)

    def test_game_str_method(self):
        """Test the string representation of the Game model."""
        game_str = str(self.game)
        expected_str = f"{self.player_1} vs {self.player_2}"
        self.assertEqual(game_str, expected_str)
