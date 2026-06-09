import urllib, base64
import io
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Team, Player, SeasonStat
from .forms import PlayerSearchForm


def team_list(request):
    teams = Team.objects.all().order_by('city')
    form = PlayerSearchForm(request.GET or None)
    search_results = None

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            search_results = Player.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            ).order_by('last_name')

    return render(request, 'analyzer/team_list.html', {
        'teams': teams,
        'form': form,
        'search_results': search_results
    })


def team_detail(request, abbr):
    team = get_object_or_404(Team, abbreviation=abbr)
    players = Player.objects.filter(team=team).order_by('last_name')
    return render(request, 'analyzer/team_detail.html', {'team': team, 'players': players})


def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    stat = SeasonStat.objects.filter(player=player, season_year=2026).first()

    context = {'player': player, 'stat': stat, 'chart': None}

    if stat:
        categories = ['PTS', 'REB', 'AST', 'STL', 'BLK']
        raw_values = [stat.points, stat.rebounds, stat.assists, stat.steals, stat.blocks]

        max_values = [35.0, 15.0, 10.0, 3.0, 3.0]
        values = [min((v / m) * 100, 100) if m > 0 else 0 for v, m in zip(raw_values, max_values)]

        labels = [f"{cat}\n{val}" for cat, val in zip(categories, raw_values)]

        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]

        values_closed = values + [values[0]]
        angles_closed = angles + [angles[0]]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        ax.set_xticks(angles)
        ax.set_xticklabels(labels)

        ax.set_yticklabels([])
        ax.set_ylim(0, 100)

        ax.plot(angles_closed, values_closed, linewidth=2, linestyle='solid', color='#ff7f0e')
        ax.fill(angles_closed, values_closed, color='#ff7f0e', alpha=0.4)

        ax.set_title(f'{player.first_name} {player.last_name}', size=14, y=1.15)

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)

        string = base64.b64encode(buf.read())
        uri = 'data:image/png;base64,' + urllib.parse.quote(string)
        context['chart'] = uri

    return render(request, 'analyzer/player_detail.html', context)