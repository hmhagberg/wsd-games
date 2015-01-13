from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404
from games.models import Game

# Create your views here.
def home(request):
	try:
		games = Game.objects.all()
	except Games.DoesNotExist:
		raise Http404
	return render_to_response('games/base_grid_card.html', {'games': games})

def games_list(request):
    raise Http404

def categories_list(request):
    raise Http404

def developers_list(request):
    raise Http404

def game(request, game_slug):
    raise Http404

def category(request, category_slug):
    raise Http404

def developer(request, developers_slug):
    raise Http404