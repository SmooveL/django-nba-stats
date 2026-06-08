from django.contrib import admin
from .models import Team, Player, SeasonStat

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'abbreviation', 'conference')
    search_fields = ('name', 'city', 'abbreviation')
    list_filter = ('conference',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team', 'position')
    search_fields = ('first_name', 'last_name')
    list_filter = ('team', 'position')

@admin.register(SeasonStat)
class SeasonStatAdmin(admin.ModelAdmin):
    list_display = ('player', 'season_year', 'games_played', 'per')
    search_fields = ('player__first_name', 'player__last_name')