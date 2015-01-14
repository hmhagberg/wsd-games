from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import Http404
from django.contrib.auth import authenticate, login

from games.forms import SignupForm


def home(request):
    return render_to_response('games/index.html')


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
    raise Http404


def developers_list(request):
    raise Http404


def game(request, game_slug):
    raise Http404


def category(request, category_slug):
    raise Http404


def developer(request, developers_slug):
    raise Http404