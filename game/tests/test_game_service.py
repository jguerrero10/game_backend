"""
Unit tests for the GameService class.
"""
from django.test import TestCase
from game.models import Player, Game, Round
from game.service.game_service import GameService


class GameServiceTestCase(TestCase):
    """Unit tests for the GameService class."""
    def setUp(self):
        """Set up the test case with initial data."""
        self.player_1 = Player.objects.create(name="Player 1")
        self.player_2 = Player.objects.create(name="Player 2")
        self.game = Game.objects.create(player_1=self.player_1, player_2=self.player_2)

    def test_update_game_score_player_2_wins(self):
        """Test updating the game score when player 2 wins a round."""
        Round.objects.create(
            game=self.game,
            player_1_move='scissors',
            player_2_move='rock',
            winner=self.player_2
        )
        self.game.refresh_from_db()
        self.assertEqual(self.game.player_2_wins, 1)

    def test_update_game_score_no_winner(self):
        """Test updating the game score when there is no winner in a round."""
        round_instance = Round.objects.create(
            game=self.game,
            player_1_move='rock',
            player_2_move='rock',
            winner=None
        )
        GameService.update_game_score(round_instance)
        self.game.refresh_from_db()
        self.assertEqual(self.game.player_1_wins, 0)
        self.assertEqual(self.game.player_2_wins, 0)

    def test_update_game_score_game_winner_final(self):
        """Test updating the game score when the game winner is determined."""
        Round.objects.create(game=self.game, player_1_move='rock', player_2_move='scissors', winner=self.player_1)
        Round.objects.create(game=self.game, player_1_move='rock', player_2_move='scissors', winner=self.player_1)
        Round.objects.create(game=self.game, player_1_move='rock', player_2_move='scissors', winner=self.player_1)

        self.game.refresh_from_db()
        self.assertTrue(self.game.is_finished)
        self.assertEqual(self.game.winner, self.player_1)

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

    def test_update_game_score_player_1_wins_final(self):
        """Test updating the game score when player 1 wins the game."""
        Round.objects.create(game=self.game, player_1_move='rock', player_2_move='scissors', winner=self.player_1)
        Round.objects.create(game=self.game, player_1_move='rock', player_2_move='scissors', winner=self.player_1)
        Round.objects.create(game=self.game, player_1_move='rock', player_2_move='scissors', winner=self.player_1)

        self.game.refresh_from_db()
        self.assertTrue(self.game.is_finished)
        self.assertEqual(self.game.winner, self.player_1)

    def test_update_game_score_player_2_wins_final(self):
        """Test updating the game score when player 2 wins the game."""
        Round.objects.create(game=self.game, player_1_move='scissors', player_2_move='rock', winner=self.player_2)
        Round.objects.create(game=self.game, player_1_move='scissors', player_2_move='rock', winner=self.player_2)
        Round.objects.create(game=self.game, player_1_move='scissors', player_2_move='rock', winner=self.player_2)

        self.game.refresh_from_db()
        self.assertTrue(self.game.is_finished)
        self.assertEqual(self.game.winner, self.player_2)
