from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render_to_response('games/index.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('..')  # TODO: Redirect user to confirmation page
    else:
        form = UserCreationForm()
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