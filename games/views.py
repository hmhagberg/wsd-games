from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import Http404
from games.models import *
from django.contrib.auth import authenticate, login
from games.forms import SignupForm
from django.template import RequestContext

context = {}

def home(request):
    try:
        games = Game.objects.all()
        categories = Category.objects.all()
        context.update({'games': games, 'categories': categories})
    except Game.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_gameCard.html', context, context_instance = RequestContext(request))


def signup(request):
    """
    Register a new user and log him in if registration was succesful.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)  # SignupForm handles fields and saving the model
        if form.is_valid():
            form.save()
            new_user = authenticate(username=request.POST["username"], password=request.POST["password1"])
            if new_user is not None:
                login(request, new_user)
            return HttpResponseRedirect('..')  # TODO: Redirect user to confirmation page
    else:
        form = SignupForm()
    return render(request, "games/signup.html", {'form': form, })


def games_list(request):
    raise Http404


def categories_list(request):
    try:
        categories = Category.objects.all()
        context.update({'categories': categories})
    except Category.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_categoryCard.html', context, context_instance = RequestContext(request))


def developers_list(request):
    try:
        developers = Developer.objects.all()
        categories = Category.objects.all()
        context.update({'developers': developers, 'categories': categories})
    except Developer.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_developerCard.html', context, context_instance = RequestContext(request))


def game(request, game_slug):
    try:
        game = Game.objects.get(slug = game_slug)
        categories = Category.objects.all()
        ownership_status = "not_owned"
        if request.user.is_authenticated():
            if hasattr(request.user, "player") and request.user.player.owns_game(game):
                ownership_status = "owned"
            elif game.developer == request.user.developer:
                ownership_status = "developer"

        context.update({'game': game, 'categories': categories, 'ownership_status': ownership_status})
    except Game.DoesNotExist:
        raise Http404
    return render_to_response('games/base_game.html', context, context_instance = RequestContext(request))

def category(request, category_slug):
    try:
        category = Category.objects.get(slug = category_slug)
        games = category.category_games.all()
        categories = Category.objects.all()
        context.update({'category': category, 'games': games, 'categories': categories, 'developer': ''})
    except Category.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_gameCard.html', context, context_instance = RequestContext(request))

def developer(request, developers_slug):
    try:
        developer = Developer.objects.get(slug = developers_slug)
        games = developer.developers_games.all()
        categories = Category.objects.all()
        context.update({'developer': developer, 'games': games, 'categories': categories, 'category': ''})
    except Developer.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_gameCard.html', context, context_instance = RequestContext(request))
