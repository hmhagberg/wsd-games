import uuid

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


class Developer(AbstractProfileModel):
    """
    Developer profile
    """
    image_url = models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')
    description = models.TextField(default='Developer description')


class SignupActivation(models.Model):
    key = models.CharField(unique=True, default=uuid.uuid4().hex, max_length=32)
    user = models.OneToOneField(User)  # TODO: Does removing this obj also remove user?
    time_sent = models.DateTimeField(auto_now_add=True)

    @property
    def has_expired(self):
        # TODO: Add meaningful expiration check
        return False


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
    price = models.DecimalField(max_digits=6, decimal_places=2)


    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
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
