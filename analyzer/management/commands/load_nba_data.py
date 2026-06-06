from django.core.management.base import BaseCommand
import pandas as pd
import requests
from io import StringIO
from analyzer.models import Team, Player, SeasonStat


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        SeasonStat.objects.all().delete()
        Player.objects.all().delete()
        Team.objects.all().delete()

        teams_data = [
            ('ATL', 'Atlanta', 'Hawks', 'East'), ('BOS', 'Boston', 'Celtics', 'East'),
            ('BKN', 'Brooklyn', 'Nets', 'East'), ('CHA', 'Charlotte', 'Hornets', 'East'),
            ('CHI', 'Chicago', 'Bulls', 'East'), ('CLE', 'Cleveland', 'Cavaliers', 'East'),
            ('DAL', 'Dallas', 'Mavericks', 'West'), ('DEN', 'Denver', 'Nuggets', 'West'),
            ('DET', 'Detroit', 'Pistons', 'East'), ('GSW', 'Golden State', 'Warriors', 'West'),
            ('HOU', 'Houston', 'Rockets', 'West'), ('IND', 'Indiana', 'Pacers', 'East'),
            ('LAC', 'Los Angeles', 'Clippers', 'West'), ('LAL', 'Los Angeles', 'Lakers', 'West'),
            ('MEM', 'Memphis', 'Grizzlies', 'West'), ('MIA', 'Miami', 'Heat', 'East'),
            ('MIL', 'Milwaukee', 'Bucks', 'East'), ('MIN', 'Minnesota', 'Timberwolves', 'West'),
            ('NOP', 'New Orleans', 'Pelicans', 'West'), ('NYK', 'New York', 'Knicks', 'East'),
            ('OKC', 'Oklahoma City', 'Thunder', 'West'), ('ORL', 'Orlando', 'Magic', 'East'),
            ('PHI', 'Philadelphia', '76ers', 'East'), ('PHX', 'Phoenix', 'Suns', 'West'),
            ('POR', 'Portland', 'Trail Blazers', 'West'), ('SAC', 'Sacramento', 'Kings', 'West'),
            ('SAS', 'San Antonio', 'Spurs', 'West'), ('TOR', 'Toronto', 'Raptors', 'East'),
            ('UTA', 'Utah', 'Jazz', 'West'), ('WAS', 'Washington', 'Wizards', 'East')
        ]

        for abbr, city, name, conf in teams_data:
            Team.objects.create(
                abbreviation=abbr,
                city=city,
                name=name,
                conference=conf
            )

        api_url = "https://raw.githubusercontent.com/ahussein0/NbaProjectML/main/2023-2024%20NBA%20Player%20Stats%20-%20Regular.csv"

        try:
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()

            csv_text = response.text
            if ';' in csv_text.split('\n')[0]:
                df = pd.read_csv(StringIO(csv_text), sep=';', engine='python')
            else:
                df = pd.read_csv(StringIO(csv_text), sep=',', engine='python')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"API Error: {e}"))
            return

        df = df.fillna(0)
        abbr_map = {'BRK': 'BKN', 'CHO': 'CHA', 'PHO': 'PHX'}
        count = 0

        for _, row in df.iterrows():
            name = str(row.get('Player', '')).strip()
            tm_abbr = str(row.get('Tm', '')).strip()

            if not name or tm_abbr == 'TOT' or name == 'Player':
                continue

            search_abbr = abbr_map.get(tm_abbr, tm_abbr)
            team = Team.objects.filter(abbreviation=search_abbr).first()

            if not team:
                continue

            try:
                g = int(float(row.get('G', 0)))
                mp = float(row.get('MP', 0.0))
                pts = float(row.get('PTS', 0.0))
                ast = float(row.get('AST', 0.0))
                trb = float(row.get('TRB', 0.0))
                stl = float(row.get('STL', 0.0))
                blk = float(row.get('BLK', 0.0))
                tov = float(row.get('TOV', 0.0))
                fgm = float(row.get('FG', 0.0))
                fga = float(row.get('FGA', 0.0))
                fg_pct = float(row.get('FG%', 0.0))
                tpm = float(row.get('3P', 0.0))
                tpa = float(row.get('3PA', 0.0))
                tp_pct = float(row.get('3P%', 0.0))
                ftm = float(row.get('FT', 0.0))
                fta = float(row.get('FTA', 0.0))
                ft_pct = float(row.get('FT%', 0.0))
            except ValueError:
                continue

            if g == 0 and mp == 0:
                continue

            clean_name = name.split('\\')[0]
            name_parts = clean_name.split(' ', 1)
            fname = name_parts[0]
            lname = name_parts[1] if len(name_parts) > 1 else ''

            player, _ = Player.objects.get_or_create(
                first_name=fname,
                last_name=lname,
                team=team,
                defaults={'position': str(row.get('Pos', 'N/A'))}
            )

            SeasonStat.objects.update_or_create(
                player=player,
                season_year=2026,
                defaults={
                    'games_played': g,
                    'minutes': mp,
                    'points': pts,
                    'assists': ast,
                    'rebounds': trb,
                    'steals': stl,
                    'blocks': blk,
                    'turnovers': tov,
                    'fgm': fgm,
                    'fga': fga,
                    'fg_pct': fg_pct,
                    'three_pm': tpm,
                    'three_pa': tpa,
                    'three_pct': tp_pct,
                    'ftm': ftm,
                    'fta': fta,
                    'ft_pct': ft_pct
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Success. Loaded: {count}"))