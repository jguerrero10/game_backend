"""
Admin configuration for the game app.
"""

from django.contrib import admin

from game.models import Player, Game, Round

admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Round)
