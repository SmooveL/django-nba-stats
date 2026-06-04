from django.shortcuts import render
from .models import Team

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'analyzer/team_list.html', {'teams': teams})

def team_detail(request, team_id):
    team = Team.objects.get(id=team_id)
    players = team.player_set.all()
    return render(request, 'analyzer/team_detail.html', {'team': team, 'players': players})