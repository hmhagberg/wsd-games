import json

from django.shortcuts import get_object_or_404

from games.models import *

response_formats = {
           # MIME type              Function to dump dict to proper format
    "json": ("application/json",    lambda x: json.dumps(x, indent=2)),
}

# NOTE: Serializers must be here before serializers-dict


def _serialize_player(player_obj, include_confidential=False):
    serialized = {"username": player_obj.user.username,
                  "slug": player_obj.slug,
                  }
    if include_confidential:
        serialized.update({"games": [{"name": o.game.name,
                                      "highscore": o.highscore, }
                                     for o in player_obj.ownerships.all()],
                           })
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
                                 game_obj.get_highscores() if o.highscore],  # Include only non-zero highscores
                  }
    if include_confidential:
        serialized.update({"url": game_obj.url,
                           "sold": game_obj.get_number_sold(),
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
                  }

    if include_confidential:
        serialized.update({"games": [{"name": g.name,
                                      "sold": g.get_number_sold(), }
                                     for g in developer_obj.games.all()]
                           })
    else:
        serialized.update({"games": [{"name": g.name, }
                                     for g in developer_obj.games.all()]
                           })

    return serialized


def _check_owner_player(player_obj, user):
    return player_obj.user == user


def _check_owner_game(game_obj, user):
    return game_obj.developer.user == user


def _check_owner_category(category_obj, user):
    return True


def _check_owner_developer(developer_obj, user):
    return developer_obj.user == user


model_info = {     # Model      Serializer func         Ownership check func    Object id field name
    "profiles":     (Player,    _serialize_player,      _check_owner_player,    "slug"),
    "games":        (Game,      _serialize_game,        _check_owner_game,      "slug"),
    "categories":   (Category,  _serialize_category,    _check_owner_category,  "slug"),
    "developers":   (Developer, _serialize_developer,   _check_owner_developer, "slug"),
}


def get_data(model_name, response_format, object_id, user):
    data = None
    serialized = ""
    model, serializer, check_owner, id_field_name = model_info[model_name]
    if object_id == "":
        objs = model.objects.all()
        data = []
        for obj in objs:
            data.append(serializer(obj))
    else:
        obj = get_object_or_404(model, **{id_field_name: object_id})
        include_confidential = check_owner(obj, user)
        data = serializer(obj, include_confidential)

    # Add other format handlers here
    if response_format == "json":
        serialized = json.dumps(data, indent=2)

    return serialized

