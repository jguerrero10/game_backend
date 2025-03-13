from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    player_1 = models.ForeignKey(Player, related_name='games_as_player_1', on_delete=models.CASCADE)
    player_2 = models.ForeignKey(Player, related_name='games_as_player_2', on_delete=models.CASCADE)
    player_1_wins = models.IntegerField(default=0)
    player_2_wins = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    winner = models.ForeignKey(Player, related_name='games_won', null=True, blank=True, on_delete=models.SET_NULL)

    def check_winner(self):
        if self.player_1_wins == 3:
            self.is_finished = True
            self.winner = self.player_1
        elif self.player_2_wins == 3:
            self.is_finished = True
            self.winner = self.player_2
        self.save()

    def __str__(self):
        return f"{self.player_1} vs {self.player_2}"


class Round(models.Model):
    MOVES = [
        ('rock', 'Rock'),
        ('paper', 'Paper'),
        ('scissors', 'Scissors'),
    ]

    game = models.ForeignKey(Game, related_name='rounds', on_delete=models.CASCADE)
    player_1_move = models.CharField(max_length=10, choices=MOVES, null=True, blank=True)
    player_2_move = models.CharField(max_length=10, choices=MOVES, null=True, blank=True)
    winner = models.ForeignKey(Player, related_name='rounds_won', null=True, blank=True, on_delete=models.SET_NULL)

    def determine_winner(self):
        if self.player_1_move == self.player_2_move:
            return None  # Empate
        if (
                (self.player_1_move == 'rock' and self.player_2_move == 'scissors') or
                (self.player_1_move == 'paper' and self.player_2_move == 'rock') or
                (self.player_1_move == 'scissors' and self.player_2_move == 'paper')
        ):
            return self.game.player_1
        return self.game.player_2

    def save(self, *args, **kwargs):
        if not self.winner:
            self.winner = self.determine_winner()

        super().save(*args, **kwargs)

        if self.winner == self.game.player_1:
            self.game.player_1_wins += 1
        elif self.winner == self.game.player_2:
            self.game.player_2_wins += 1

        self.game.check_winner()
