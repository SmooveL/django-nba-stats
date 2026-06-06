from django.shortcuts import render, get_object_or_404
from .models import Team, Player

def team_list(request):
    teams = Team.objects.all().order_by('name')
    return render(request, 'analyzer/team_list.html', {'teams': teams})

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    players = team.player_set.prefetch_related('seasonstat_set').all()
    return render(request, 'analyzer/team_detail.html', {'team': team, 'players': players})