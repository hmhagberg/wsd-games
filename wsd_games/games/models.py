from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    url = models.URLField()
    image_url = models.URLField(blank=True, default='')
    developer = models.ForeignKey(Developer, related_name='developers_games')
    categories = models.ManyToManyField(Category, related_name='category_games')

    class Meta:
        ordering = ["name"]

    @property
    def slug(self):
        return self.name.lower()  # TODO: Convert name to slug properly (special chars, whitespace etc)

    def __str__(self):
        return self.name


class Ownership(models.Model):
    RATING_OPTIONS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),)
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player, related_name='ownerships')
    highscore = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(choices=RATING_OPTIONS)

    def __str__(self):
        return self.player.name + " owns " + self.game.name

    def set_new_score(self, new_score):
        """Returns True if the given score is a new highscore"""
        if new_score > self.highscore:
            self.highscore = new_score
            self.save()
            return True
        else:
            return False


