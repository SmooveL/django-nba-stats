from django.contrib import admin
from .models import Team, Player, SeasonStat

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(SeasonStat)