from social.pipeline.partial import partial
from django.shortcuts import redirect
from django.contrib import messages

from games.utils import set_query_params
from games.models import Player


@partial
def ask_username(backend, is_new=False, *args, **kwargs):
    """
    Ask user for site-specific username if user logs in for the first time.
    """
    if is_new:
        data = backend.strategy.request_data()
        if data.get("username_from_user") is None:  # Display the form
            response = redirect("social_select_username")
            response = set_query_params(response, backend=backend.name)
            return response
        else:  # User has selected username -> continue pipeline
            return {"username": data.get("username_from_user")}


def save_player_profile(user, is_new=False, *args, **kwargs):
    """
    Save player's profile information.
    """
    if is_new:
        player = Player(user=user)
        player.save()


def set_login_message(strategy, is_new=False, *args, **kwargs):
    """
    Set 'login successful' message like in regular login.
    """
    if is_new:
        messages.success(strategy.request, "Congratulations! Your account has been created.")
    else:
        messages.success(strategy.request, "You have logged in.")
