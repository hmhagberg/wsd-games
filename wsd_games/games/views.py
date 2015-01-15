from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404
from games.models import *

# Create your views here.
def home(request):
	try:
		games = Game.objects.all()
		categories = Category.objects.all()
	except Game.DoesNotExist:
		raise Http404
	return render_to_response('games/base_grid_gameCard.html', {'games': games, 'categories': categories})

def games_list(request):
    raise Http404

def categories_list(request):
	try:
		categories = Category.objects.all()
	except Category.DoesNotExist:
		raise Http404
	return render_to_response('games/base_grid_categoryCard.html', {'categories': categories})

def developers_list(request):
	try:
		developers = Developer.objects.all()
		categories = Category.objects.all()
	except Developer.DoesNotExist:
		raise Http404
	return render_to_response('games/base_grid_developerCard.html', {'developers': developers, 'categories': categories})

def game(request, game_slug):
	try:
		game = Game.objects.get(id = game_slug)
		categories = Category.objects.all()
	except Game.DoesNotExist:
		raise Http404
	return render_to_response('games/base_game.html', {'game': game, 'categories': categories})

def category(request, category_slug):
	try:
		category = Category.objects.get(id = category_slug)
		games = Game.objects.filter(categories = category_slug)
		categories = Category.objects.all()
	except Category.DoesNotExist:
		raise Http404
	return render_to_response('games/base_grid_gameCard.html', {'category': category, 'games': games, 'categories': categories})

def developer(request, developers_slug):
	try:
		developer = Developer.objects.get(id = developers_slug)
		games = Game.objects.filter(developer = developers_slug)
		categories = Category.objects.all()
	except Developer.DoesNotExist:
		raise Http404
	return render_to_response('games/base_grid_gameCard.html', {'developer': developer, 'games': games, 'categories': categories})