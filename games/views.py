import uuid
import hashlib

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.views.generic import View, FormView
from django.template import RequestContext

from games.models import *
from games.forms import SignupForm, PaymentForm, UsernameForm
import wsd_games.settings

context = {}


def home(request):
    try:
        games = Game.objects.all()
        categories = Category.objects.all()
        context.update({'games': games, 'categories': categories, 'category': '', 'developer': ''})
    except Game.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_gameCard.html', context, context_instance=RequestContext(request))


class SignupView(FormView):
    template_name = "games/auth/signup.html"
    form_class = SignupForm
    success_url = ".."  # TODO: Redirect user to confirmation page

    def form_valid(self, form):
        form.save()
        new_user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
        if new_user is not None:
            login(self.request, new_user)
        return super(SignupView, self).form_valid(form)


def social_select_username(request, backend):
    """
    Username selection view for social auth
    """
    form = UsernameForm()
    return render_to_response("games/auth/select_username.html", {"form": form, "backend": backend},
                              context_instance=RequestContext(request))


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
    ownership = None
    if request.user.is_authenticated():
        if hasattr(request.user, "player"):
            if request.user.player.owns_game(game):
                ownership_status = "owned"
                ownership = request.user.player.ownerships.get(player=request.user.player, game=game)
        elif game.developer == request.user.developer:
            ownership_status = "developer"
    context.update({'game': game, 'categories': categories, 'ownership_status': ownership_status, 'ownership':
        ownership})

    # Handle game messages
    if request.method == 'POST':
        if request.POST['messageType'] == "SCORE":
            ownership.set_new_score(int(request.POST['score']))
        elif request.POST['messageType'] == "SAVE":
            ownership.save_game(int(request.POST["gameState[score]"]), ','.join(request.POST.getlist("gameState[playerItems][]")))

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

    DOMAIN = "http://localhost:8000/"
    SUCCESS_URL = DOMAIN + "payment/success"
    CANCEL_URL = DOMAIN + "payment/cancel"
    ERROR_URL = DOMAIN + "payment/error"

    def get(self, request, payment_success, payment_cancel, *args, **kwargs):
        pid = request.GET["pid"]
        ref = request.GET["ref"]
        request_checksum = request.GET["checksum"]
        ownership = get_object_or_404(Ownership, payment_pid=pid)
        context = {"player": ownership.player, "game": ownership.game}

        if payment_success is not None:
            checksumstr = "pid=%s&ref=%s&token=%s" % (pid, ref, settings.SID_KEY)
            checksum = hashlib.md5(checksumstr.encode("ascii")).hexdigest()
            if checksum == request_checksum:
                ownership.payment_completed = True
                ownership.payment_ref = ref
                ownership.save()
                return render_to_response("games/payment/payment_success.html", context)
        elif payment_cancel is not None:
            ownership.delete()
            return render_to_response("games/payment/payment_cancel.html", context)

        return render_to_response("games/payment/payment_error.html")

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

        # Check for old payments that haven't been completed properly (either via /payment/success/ or payment/cancel/)
        try:
            old_ownership = request.user.player.ownerships.all().get(game=game)
            if old_ownership.payment_completed:
                return render_to_response("games/payment/payment_error.html")
            old_ownership.delete()
        except Ownership.DoesNotExist:
            pass

        ownership = Ownership(game=game, player=request.user.player, payment_pid=pid)
        ownership.save()
        return render_to_response("games/payment/payment.html", {"game": game, "form": form},
                                  context_instance=RequestContext(request))
