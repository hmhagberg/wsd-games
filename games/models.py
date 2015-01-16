from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from wsd_games import settings


class AbstractSlugModel(models.Model):
    """
    Abstract base model for models with name and slug. Upon creation of new object the slug is created based on
    object name.
    """

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(AbstractSlugModel, self).save(*args, **kwargs)


class AbstractProfileModel(models.Model):
    """
    Abstract base model for models that need to be linked to Django auth's User model
    """

    user = models.OneToOneField(User)
    slug = models.SlugField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        super(AbstractProfileModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Player(AbstractProfileModel):
    """
    Player profile
    """

    def owns_game(self, game):
        return game in self.ownerships.all()


class Developer(AbstractProfileModel):
    """
    Developer profile
    """
    image_url = models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')
    description = models.TextField(default='Developer description')


class Category(AbstractSlugModel):
    image_url = models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')
    description = models.TextField(default='Category description')

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Game(AbstractSlugModel):
    description = models.TextField(default='Game description')
    url = models.URLField()
    image_url = models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')
    developer = models.ForeignKey(Developer, related_name='developers_games')
    categories = models.ManyToManyField(Category, related_name='category_games')

    class Meta:
        ordering = ["name"]

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


