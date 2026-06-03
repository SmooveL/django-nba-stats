from django.shortcuts import render
from .models import Team

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'analyzer/team_list.html', {'teams': teams})