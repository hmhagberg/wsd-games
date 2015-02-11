from social.pipeline.partial import partial
from django.shortcuts import redirect
from django.contrib import messages

from games.utils import set_query_params
from games.models import Player


@partial
def ask_username(backend, is_new=False, *args, **kwargs):
    if is_new:
        data = backend.strategy.request_data()
        if data.get("username_from_user") is None:
            response = redirect("social_select_username")
            response = set_query_params(response, backend=backend.name)
            return response
        else:
            return {"username": data.get("username_from_user")}


def save_player_profile(user, is_new=False, *args, **kwargs):
    if is_new:
        player = Player(user=user)
        player.save()


def set_login_message(strategy, *args, **kwargs):
    messages.success(strategy.request, "You have logged in.")