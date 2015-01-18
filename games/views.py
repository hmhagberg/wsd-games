import uuid
import hashlib

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.template import RequestContext

from games.models import *
from games.forms import SignupForm, PaymentForm
import wsd_games.settings

context = {}


def home(request):
    try:
        games = Game.objects.all()
        categories = Category.objects.all()
        context.update({'games': games, 'categories': categories})
    except Game.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_gameCard.html', context, context_instance=RequestContext(request))


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
    return home(request)


def categories_list(request):
    try:
        categories = Category.objects.all()
        context.update({'categories': categories})
    except Category.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_categoryCard.html', context, context_instance=RequestContext(request))


def developers_list(request):
    try:
        developers = Developer.objects.all()
        categories = Category.objects.all()
        context.update({'developers': developers, 'categories': categories})
    except Developer.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_developerCard.html', context, context_instance=RequestContext(request))


def game(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    categories = Category.objects.all()
    ownership_status = "not_owned"
    if request.user.is_authenticated():
        if hasattr(request.user, "player"):
            if request.user.player.owns_game(game):
                ownership_status = "owned"
        elif game.developer == request.user.developer:
            ownership_status = "developer"

    context.update({'game': game, 'categories': categories, "user": request.user, 'ownership_status': ownership_status})
    return render_to_response('games/base_game.html', context, context_instance=RequestContext(request))


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    games = category.category_games.all()
    categories = Category.objects.all()
    context.update({'category': category, 'games': games, 'categories': categories, 'developer': ''})

    return render_to_response('games/base_grid_gameCard.html', context, context_instance=RequestContext(request))


def developer(request, developers_slug):
    developer = get_object_or_404(Developer, slug=developers_slug)
    games = developer.developers_games.all()
    categories = Category.objects.all()
    context.update({'developer': developer, 'games': games, 'categories': categories, 'category': ''})
    return render_to_response('games/base_grid_gameCard.html', context, context_instance=RequestContext(request))


class PaymentView(View):
    http_method_names = ["post"]

    SUCCESS_URL = "http://localhost:8000/payment/success"
    CANCEL_URL = "http://localhost:8000/payment/cancel"
    ERROR_URL = "http://localhost:8000/payment/error"

    def post(self, request, *args, **kwargs):
        game = get_object_or_404(Game, id=request.POST["game_id"])

        pid = uuid.uuid4().hex
        sid = settings.SID
        amount = game.price
        checksumstr = "pid=%s&sid=%s&amount=%s&token=%s" % (pid, sid, amount, settings.SID_KEY)
        checksum = hashlib.md5(checksumstr.encode("ascii")).hexdigest()

        values = {"pid": pid,
                  "sid": sid,
                  "success_url": PaymentView.SUCCESS_URL,
                  "cancel_url": PaymentView.CANCEL_URL,
                  "error_url": PaymentView.ERROR_URL,
                  "amount": amount,
                  "checksum": checksum}

        form = PaymentForm()
        form.set_values(values)

        return render_to_response("games/payment.html", {"game": game, "form": form}, context_instance=RequestContext(
            request))
