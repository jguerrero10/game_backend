"""
Unit tests for the Game API views.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from game.models import Player, Game, Round


class GameAPITestCase(APITestCase):
    """Unit tests for the Game API views."""

    def setUp(self):
        """Set up the test case with initial data."""
        self.player_1 = Player.objects.create(name="Player 1")
        self.player_2 = Player.objects.create(name="Player 2")
        self.game = Game.objects.create(player_1=self.player_1, player_2=self.player_2)

    def test_create_player(self):
        """Test creating a new player."""
        url = reverse('player-list')
        data = {"name": "New Player"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 3)

    def test_create_game(self):
        """Test creating a new game."""
        url = reverse('game-list')
        data = {"player_1": self.player_1.id, "player_2": self.player_2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_round_and_check_winner(self):
        """Test creating a new round and checking the winner."""
        url = reverse('round-list')
        data = {"game": self.game.id, "player_1_move": "rock", "player_2_move": "scissors"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        round_obj = Round.objects.get(id=response.data['id'])
        self.assertEqual(round_obj.winner, self.player_1)

    def test_game_winner_after_3_rounds(self):
        """Test determining the game winner after 3 rounds."""
        url = reverse('round-list')

        self.client.post(url, {"game": self.game.id, "player_1_move": "rock", "player_2_move": "scissors"})
        self.client.post(url, {"game": self.game.id, "player_1_move": "rock", "player_2_move": "scissors"})
        self.client.post(url, {"game": self.game.id, "player_1_move": "rock", "player_2_move": "scissors"})

        self.game.refresh_from_db()
        self.assertTrue(self.game.is_finished)
        self.assertEqual(self.game.winner, self.player_1)

    def test_no_round_after_game_finished(self):
        """Test creating a new round after the game has finished."""
        Round.objects.create(game=self.game, player_1_move='rock', player_2_move='scissors')
        Round.objects.create(game=self.game, player_1_move='rock', player_2_move='scissors')
        Round.objects.create(game=self.game, player_1_move='rock', player_2_move='scissors')

        url = reverse('round-list')
        data = {"game": self.game.id, "player_1_move": "paper", "player_2_move": "rock"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_cannot_create_round_for_finished_game(self):
        """Test creating a new round for a finished game."""
        self.game.player_1_wins = 3
        self.game.is_finished = True
        self.game.save()

        url = reverse('round-list')
        data = {
            "game": self.game.id,
            "player_1_move": "rock",
            "player_2_move": "scissors"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_create_round_with_invalid_data(self):
        """Test creating a new round with invalid data."""
        url = reverse('round-list')
        data = {"game": self.game.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('player_1_move', response.data)
        self.assertIn('player_2_move', response.data)

        data = {"game": self.game.id, "player_1_move": "invalid_move", "player_2_move": "rock"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('player_1_move', response.data)

    def test_create_round_with_non_existent_game(self):
        """Test creating a new round with a non-existent game."""
        url = reverse('round-list')

        data = {
            "game": 999,
            "player_1_move": "rock",
            "player_2_move": "scissors"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "El juego no existe.")
