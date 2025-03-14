"""Models for the game app."""

from django.db import models

from game.service.game_service import GameService


class Player(models.Model):
    """Model representing a player in the game."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """Return the name of the player."""
        return self.name


class Game(models.Model):
    """Model representing a game between two players."""

    player_1 = models.ForeignKey(Player, related_name='games_as_player_1', on_delete=models.CASCADE)
    player_2 = models.ForeignKey(Player, related_name='games_as_player_2', on_delete=models.CASCADE)
    player_1_wins = models.IntegerField(default=0)
    player_2_wins = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    winner = models.ForeignKey(Player, related_name='games_won', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        """Return a string representation of the game."""
        return f"{self.player_1} vs {self.player_2}"


class Round(models.Model):
    """Model representing a round in a game."""

    MOVES = [
        ('rock', 'Rock'),
        ('paper', 'Paper'),
        ('scissors', 'Scissors'),
    ]

    game = models.ForeignKey(Game, related_name='rounds', on_delete=models.CASCADE)
    player_1_move = models.CharField(max_length=10, choices=MOVES, null=True, blank=True)
    player_2_move = models.CharField(max_length=10, choices=MOVES, null=True, blank=True)
    winner = models.ForeignKey(Player, related_name='rounds_won', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        """Save the round and update the game's winner."""
        if not self.winner:
            self.winner = GameService.determine_round_winner(self.player_1_move, self.player_2_move, self.game)

        super().save(*args, **kwargs)

        GameService.update_game_score(self)
