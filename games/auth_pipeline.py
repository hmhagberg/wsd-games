from social.pipeline.partial import partial
from django.shortcuts import redirect

from .models import Player


@partial
def ask_username(backend, is_new=False, *args, **kwargs):
    if is_new:
        data = backend.strategy.request_data()
        if data.get("username_from_user") is None:
            return redirect("social_select_username", backend.name)
        else:
            return {"username": data.get("username_from_user")}


def save_player_profile(user, is_new=False, *args, **kwargs):
    if is_new:
        player = Player(user=user)
        player.save()