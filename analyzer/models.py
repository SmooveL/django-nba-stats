from django.db import models

class Team(models.Model):
    abbreviation = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    conference = models.CharField(max_length=50)

class Player(models.Model):
    api_id = models.IntegerField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)

class SeasonStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season_year = models.IntegerField()
    games_played = models.IntegerField(default=0)
    minutes = models.FloatField(default=0.0)
    points = models.FloatField(default=0.0)
    rebounds = models.FloatField(default=0.0)
    assists = models.FloatField(default=0.0)
    steals = models.FloatField(default=0.0)
    blocks = models.FloatField(default=0.0)
    turnovers = models.FloatField(default=0.0)
    fgm = models.FloatField(default=0.0)
    fga = models.FloatField(default=0.0)
    fg_pct = models.FloatField(default=0.0)
    three_pm = models.FloatField(default=0.0)
    three_pa = models.FloatField(default=0.0)
    three_pct = models.FloatField(default=0.0)
    ftm = models.FloatField(default=0.0)
    fta = models.FloatField(default=0.0)
    ft_pct = models.FloatField(default=0.0)

    @property
    def per(self):
        missed_fg = self.fga - self.fgm
        missed_ft = self.fta - self.ftm
        val = (self.points + self.rebounds + self.assists + self.steals + self.blocks) - (missed_fg + missed_ft + self.turnovers)
        return round(val, 1)