from django.http import HttpResponseRedirect
from social.pipeline.partial import partial
from django.shortcuts import redirect

from .models import Player


@partial
def ask_username(backend, is_new=False, *args, **kwargs):
    if is_new:
        data = backend.strategy.request_data()
        if data.get("username_from_user") is None:
            response = redirect("social_select_username")

            # Set query parameter backend to backend.name
            response["Location"] = response["Location"].rstrip("/")
            response["Location"] += "?backend=" + backend.name
            return response
        else:
            return {"username": data.get("username_from_user")}


def save_player_profile(user, is_new=False, *args, **kwargs):
    if is_new:
        player = Player(user=user)
        player.save()