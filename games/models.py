import uuid
import hmac
import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator

from games.utils import unique_slugify


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
        unique_slugify(self, self.name)
        return super(AbstractSlugModel, self).save(*args, **kwargs)

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name


class WsdGamesUser(AbstractUser):
    """
    Custom user model
    """
    api_token = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Set token only if this is first time object is saved()
            self.api_token = self.generate_new_token()
        return super(WsdGamesUser, self).save(*args, **kwargs)

    def natural_key(self):
        return self.username

    def is_player(self):
        return hasattr(self, "player")

    def is_developer(self):
        return hasattr(self, "developer")

    def is_social_auth_user(self):
        """
        Check if user is authenticated through social auth by checking if there's record of her in social auth DB
        tables.
        """
        try:
            self.social_auth.get(user=self)
            return True
        except ObjectDoesNotExist:
            return False

    def generate_new_token(self):
        """
        Generate new API token based on time and user's username
        """
        msg = str(datetime.datetime.now())+self.username
        h = hmac.new(settings.API_SECRET, msg.encode("ascii"), "sha1")
        return h.hexdigest()


class Player(models.Model):
    """
    Player profile
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    slug = models.SlugField()
    about_me = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.user.username)
        super(Player, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("games.views.profiles", args=[self.slug])

    def owns_game(self, game):
        try:
            self.ownerships.get(game=game)
            return True
        except Ownership.DoesNotExist:
            return False

    def games(self):
        """
        Return list of games this player owns
        """
        return [o.game for o in self.ownerships.all()]


class Developer(AbstractSlugModel):
    """
    Developer profile
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    image_url = models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')
    description = models.TextField(default='Developer description')

    def get_absolute_url(self):
        return reverse("games.views.developer_detail", args=[self.slug])


class SignupActivation(models.Model):
    key = models.CharField(unique=True, max_length=32)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    time_sent = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.key = uuid.uuid4().hex
        super(SignupActivation, self).save(*args, **kwargs)

    def has_expired(self):
        diff = datetime.datetime.now() - self.time_sent
        diff_hours = diff.total_seconds() / 3600
        return diff_hours > settings.ACTIVATION_EXPIRATION_HOURS


class Category(AbstractSlugModel):
    image_url = models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')
    description = models.TextField(default='Category description')

    def get_absolute_url(self):
        return reverse("games.views.category_detail", args=[self.slug])


class Game(AbstractSlugModel):
    description = models.TextField(default='Game description')
    url = models.URLField()
    image_url = models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')
    developer = models.ForeignKey(Developer, related_name='games')
    categories = models.ManyToManyField(Category, related_name='games')
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    publish_date = models.DateField(auto_now_add=True, default=datetime.date.today())

    def get_absolute_url(self):
        return reverse("games.views.game_detail", args=[self.slug])

    """
    Returns Ownerships with highest scores for this game
    """
    def get_highscores(self, limit=10, nonzero_only=True):
        if nonzero_only:
            return self.ownerships.all().filter(highscore__gt=0)[:limit]
        else:
            return self.ownerships.all()[:limit]

    def get_sales_count(self, time_scope=0):
        if time_scope == 0:
            return self.ownerships.count()
        else:
            return self.ownerships.filter(timestamp__lte=datetime.datetime.now()+datetime.timedelta(hours=time_scope)).count()


class Ownership(models.Model):
    """
    Models which links (owned) games to players. Related data (e.g. user's highscore) is also stored here.
    """

    game = models.ForeignKey(Game, related_name="ownerships")
    player = models.ForeignKey(Player, related_name='ownerships')
    highscore = models.PositiveIntegerField(default=0)
    saved_score = models.PositiveIntegerField(default=0)
    saved_data = models.TextField(default='[]')
    timestamp = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())

    class Meta:
        ordering = ["-highscore"]

    def __str__(self):
        return self.player.user.username + " owns " + self.game.name

    def set_new_score(self, new_score):
        """
        Set new highscore if new_score is higher than existing highscore. Return True if new highscore was set.
        """
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


class Payment(models.Model):
    """
    Payment data
    """
    game = models.ForeignKey(Game, related_name="sales")
    player = models.ForeignKey(Player, related_name="payments")

    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    pid = models.CharField(max_length=32, unique=True)
    ref = models.CharField(max_length=32, blank=True)
