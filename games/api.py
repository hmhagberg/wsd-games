import json

from django.shortcuts import get_object_or_404

from games.models import *

content_types = {
    "json": "application/json",
}

# NOTE: Serializers must be here before serializers-dict


def _serialize_player(player_obj, include_confidential=False):
    serialized = {"username": player_obj.user.username,
                  "slug": player_obj.slug,
                  }
    if include_confidential:
        serialized.update({"games": [game.name for game in player_obj.games()], })
    return serialized


def _serialize_game(game_obj, include_confidential=False):
    serialized = {"name": game_obj.name,
                  "slug": game_obj.slug,
                  "description": game_obj.description,
                  "image_url": game_obj.image_url,
                  "developer": game_obj.developer.name,
                  "categories": [c.name for c in game_obj.categories.all()],
                  "price": str(game_obj.price),  # Default JSON encoder doesn't support Decimal
                  "highscores": [{"username": o.player.user.username, "score": o.highscore} for o in
                                 game_obj.ownerships.all()],
                  }
    if include_confidential:
        serialized.update({"url": game_obj.url,
                           "sales": len(game_obj.ownerships.all()),
                           })
    return serialized


def _serialize_category(category_obj, include_confidential=False):
    serialized = {"name": category_obj.name,
                  "slug": category_obj.slug,
                  "image_url": category_obj.image_url,
                  "description": category_obj.description,
                  "games": [g.name for g in category_obj.games.all()],
                  }

    return serialized


def _serialize_developer(developer_obj, include_confidential=False):
    serialized = {"name": developer_obj.name,
                  "slug": developer_obj.slug,
                  "image_url": developer_obj.image_url,
                  "description": developer_obj.description,
                  "games": [g.name for g in developer_obj.games.all()],
                  }

    return serialized


model_info = {
    "profiles": (Player, _serialize_player, "slug"),
    "games": (Game, _serialize_game, "slug"),
    "categories": (Category, _serialize_category, "slug"),
    "developers": (Developer, _serialize_developer, "slug"),
    }


def get_data(model_name, format, id, api_token):
    data = None
    model, serializer, id_field_name = model_info[model_name]
    if id == "":
        objs = model.objects.all()
        data = []
        for obj in objs:
            data.append(serializer(obj))
    else:
        obj = get_object_or_404(model, **{id_field_name: id})
        # TODO: Implement ownership check based on api_token
        data = serializer(obj, include_confidential=True)

    if format == "json":
        serialized = json.dumps(data, indent=2)
    else:
        serialized = ""

    return serialized



