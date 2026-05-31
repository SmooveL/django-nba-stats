from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    conference = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    api_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SeasonStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season_year = models.IntegerField()
    games_played = models.IntegerField(default=0)
    minutes = models.FloatField(default=0.0)
    points = models.FloatField(default=0.0)
    assists = models.FloatField(default=0.0)
    rebounds = models.FloatField(default=0.0)
    calculated_per = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.player} - {self.season_year}"