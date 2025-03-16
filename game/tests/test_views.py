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
        self.player_3 = Player.objects.create(name="Player 3")
        self.player_4 = Player.objects.create(name="Player 4")
        self.player_5 = Player.objects.create(name="Player 5")
        self.player_6 = Player.objects.create(name="Player 6")

        for _ in range(10):
            Game.objects.create(player_1=self.player_1, player_2=self.player_2, winner=self.player_1)

        for _ in range(8):
            Game.objects.create(player_1=self.player_2, player_2=self.player_3, winner=self.player_2)

        for _ in range(7):
            Game.objects.create(player_1=self.player_3, player_2=self.player_4, winner=self.player_3)

        for _ in range(5):
            Game.objects.create(player_1=self.player_4, player_2=self.player_5, winner=self.player_4)

        for _ in range(3):
            Game.objects.create(player_1=self.player_5, player_2=self.player_6, winner=self.player_5)

        for _ in range(2):
            Game.objects.create(player_1=self.player_6, player_2=self.player_1, winner=self.player_6)

        self.game = Game.objects.create(player_1=self.player_1, player_2=self.player_2)

    def test_create_player(self):
        """Test creating a new player."""
        url = reverse('player-list')
        data = {"name": "New Player"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 7)

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

    def test_top_winners_returns_top_5_players(self):
        """Verifica que el endpoint retorne el top 5 de jugadores."""
        url = reverse('player-top-winners')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        expected_names = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5']
        actual_names = [player['name'] for player in response.data]

        self.assertEqual(actual_names, expected_names)

    def test_top_winners_returns_empty_list_when_no_players(self):
        """Verifica que el endpoint retorne una lista vacía si no hay jugadores."""
        Player.objects.all().delete()

        url = reverse('player-top-winners')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_top_winners_rejects_post_request(self):
        """Verifica que el endpoint rechace métodos POST."""
        url = reverse('player-top-winners')
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
