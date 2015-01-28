import uuid

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse


class AbstractSlugModel(models.Model):
    """
    Abstract base model for models with name and slug. Upon creation of new object the slug is created based on
    object name.
    """

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField()

    class Meta:
        abstract = True
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(AbstractSlugModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class WsdGamesUser(AbstractUser):

    def __getattr__(self, item):
        if item == "player" or item == "developer" or item.endswith("_cache"):  # Prevents infinite recursion
            raise AttributeError("%r object has no attribute %r" % (
                type(self).__name__, item))
        elif hasattr(self, "player"):
            get_from = self.player
        else:
            get_from = self.developer

        attr = getattr(get_from, item)
        if attr is None:
            raise AttributeError("%r object has no attribute %r" % (
                type(self).__name__, item))
        else:
            return attr

    def is_player(self):
        return hasattr(self, "player")

    def is_developer(self):
        return hasattr(self, "developer")


class Player(models.Model):
    """
    Player profile
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        super(Player, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("games.views.profiles", args=[self.slug])

    def owns_game(self, game):
        try:
            ownership = self.ownerships.all().get(game=game)
            return ownership.payment_completed
        except Ownership.DoesNotExist:
            return False

    def games(self):
        games = []
        for i in self.ownerships.all():
            if i.payment_completed:
                games.append(i.game)
        return games


class Developer(AbstractSlugModel):
    """
    Developer profile
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    image_url = models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')
    description = models.TextField(default='Developer description')

    def get_absolute_url(self):
        return reverse("games.views.developer", args=[self.slug])


class SignupActivation(models.Model):
    key = models.CharField(unique=True, default=uuid.uuid4().hex, max_length=32)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)  # TODO: Does removing this obj also remove user?
    time_sent = models.DateTimeField(auto_now_add=True)

    @property
    def has_expired(self):
        # TODO: Add meaningful expiration check
        return False


class Category(AbstractSlugModel):
    image_url = models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')
    description = models.TextField(default='Category description')

    def get_absolute_url(self):
        return reverse("games.views.category", args=[self.slug])


class Game(AbstractSlugModel):
    description = models.TextField(default='Game description')
    url = models.URLField()
    image_url = models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')
    developer = models.ForeignKey(Developer, related_name='developers_games')
    categories = models.ManyToManyField(Category, related_name='category_games')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def get_absolute_url(self):
        return reverse("games.views.game", args=[self.slug])

    def get_highscores(self, limit=10):
        highscores = []
        for i in self.ownerships.all():
            if i.payment_completed:
                highscores.append(i)
        return highscores[:limit]


class Ownership(models.Model):
    RATING_OPTIONS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),)
    game = models.ForeignKey(Game, related_name="ownerships")
    player = models.ForeignKey(Player, related_name='ownerships')
    highscore = models.PositiveIntegerField(default=0)
    saved_score = models.PositiveIntegerField(default=0)
    saved_data = models.TextField(default='[]')
    rating = models.PositiveIntegerField(null=True, choices=RATING_OPTIONS)

    # Payment information
    payment_timestamp = models.DateTimeField(auto_now_add=True)
    payment_completed = models.BooleanField(default=False)
    payment_pid = models.CharField(max_length=32, unique=True)
    payment_ref = models.CharField(max_length=32, blank=True)

    class Meta:
        ordering = ["-highscore"]

    def __str__(self):
        return self.player.user.username + " owns " + self.game.name

    def set_new_score(self, new_score):
        """Returns True if the given score is a new highscore"""
        if new_score > self.highscore:
            self.highscore = new_score
            self.save()
            return True
        else:
            return False

    def save_game(self, score, data):
        self.saved_score = score
        self.saved_data = data
        self.save()
