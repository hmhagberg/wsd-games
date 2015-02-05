import hashlib
import json

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render_to_response, render
from django.http import Http404, HttpResponse
from django.views.generic import View, FormView
from django.template import RequestContext

from games import api
from games.models import *
from games.forms import *

context = {}


def home(request):
    try:
        games = Game.objects.all()
        categories = Category.objects.all()
        context.update({'games': games, 'categories': categories, 'category': '', 'developer': '', 'title': ''})
    except Game.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_gameCard.html', context, context_instance=RequestContext(request))


class LoginView(FormView):
    template_name = "games/auth/base_login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("home")
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect("home")


class SignupView(View):

    def get(self, request, dev_signup, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("home")

        if dev_signup is None:
            form = PlayerSignupForm()
        else:
            form = DeveloperSignupForm()

        return render(request, "games/auth/base_signup.html", {"form": form, "dev_signup": dev_signup})

    def post(self, request, dev_signup, *args, **kwargs):
        if dev_signup is None:
            form = PlayerSignupForm(request.POST)
        else:
            form = DeveloperSignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            link = SignupView.send_activation_mail(user)
            return render(request, "games/auth/activate_pending.html", {"username": user.username, "link": link})
        else:
            return render(request, "games/auth/base_signup.html", {"form": form, "dev_signup": dev_signup})

    @staticmethod
    def send_activation_mail(user):
        activation = SignupActivation(user=user)
        activation.save()
        # TODO: Write better message, possibly in separate file?
        activation_link = "{domain}/signup/activate/{key}".format(domain=settings.DOMAIN, key=activation.key)
        message = "Thank you for signing up, {username}\n" \
                  "To activate your account click the following link: {link}\n" \
                  "The link expires in {expires_in} hours".format(username=user.username, link=activation_link,
                                                                  expires_in=settings.ACTIVATION_EXPIRATION_HOURS)
        send_mail("WSD Games Account Activation", message, "noreply@wsd-games.fi", [user.email])
        return activation_link


class GamePublishingView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            form = GamePublishingForm()
            return render(request, "games/auth/base_signup.html", {"form": form,})

    def post(self, request, *args, **kwargs):
        form = GamePublishingForm(request.POST)

        if form.is_valid():
            game = form.save(commit=False)
            game.developer = request.user.developer
            game.save()
            return redirect("games/"+game.slug)
        else:
            return render(request, "games/auth/base_signup.html", {"form": form,})


def signup_activation(request, activation_key):
    if request.user.is_authenticated():
        return redirect("home")

    # TODO: Is it better to return 404 or redirect to home?
    confirmation = get_object_or_404(SignupActivation, key=activation_key)
    if confirmation.has_expired():
        confirmation.delete()
        return render(request, "games/auth/activate_expired.html")

    user = confirmation.user
    user.is_active = True
    user.save()
    confirmation.delete()
    return render(request, "games/auth/activate.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def profiles(request, profile_slug):
    profile = get_object_or_404(Player, slug=profile_slug)
    categories = Category.objects.all()
    context.update({'profile': profile, 'categories': categories})

    return render_to_response('games/base_profile.html', context, context_instance=RequestContext(request))


def my_games(request):
    try:
        games = request.user.player.games()
        categories = Category.objects.all()
        context.update({'games': games, 'categories': categories, 'category': '', 'developer': '', 'title': 'My'})
    except Game.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_gameCard.html', context, context_instance=RequestContext(request))


def social_select_username(request, backend):
    """
    Username selection view for social auth
    """
    form = UsernameForm()
    return render_to_response("games/auth/base_selectUsername.html", {"form": form, "backend": backend},
                              context_instance=RequestContext(request))


def games_list(request):
    return home(request)


def categories_list(request):
    try:
        categories = Category.objects.all().order_by('name')
        context.update({'categories': categories})
    except Category.DoesNotExist:
        raise Http404
    return render_to_response('games/base_grid_categoryCard.html', context, context_instance=RequestContext(request))


def developers_list(request):
    try:
        developers = Developer.objects.all().order_by('slug')
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
    games = category.games.all()
    categories = Category.objects.all()
    context.update({'category': category, 'games': games, 'categories': categories, 'developer': '', 'title': ''})

    return render_to_response('games/base_grid_gameCard.html', context, context_instance=RequestContext(request))


def developer(request, developers_slug):
    developer = get_object_or_404(Developer, slug=developers_slug)
    games = developer.games.all()
    categories = Category.objects.all()
    context.update({'developer': developer, 'games': games, 'categories': categories, 'category': '', 'title': ''})
    return render_to_response('games/base_grid_gameCard.html', context, context_instance=RequestContext(request))


class PaymentView(View):

    def get(self, request, payment_status, *args, **kwargs):
        pid = request.GET.get("pid")
        ref = request.GET.get("ref")
        request_checksum = request.GET.get("checksum")
        if not (pid and ref and request_checksum):
            raise Http404
        payment = get_object_or_404(Payment, pid=pid)
        context = {"player": payment.player, "game": payment.game}

        if payment_status == "success":
            checksumstr = "pid=%s&ref=%s&token=%s" % (pid, ref, settings.SID_KEY)
            checksum = hashlib.md5(checksumstr.encode("ascii")).hexdigest()
            if checksum == request_checksum:
                payment.completed = True
                payment.ref = ref
                payment.save()

                ownership = Ownership(game=payment.game, player=payment.player)
                ownership.save()
                return render(request, "games/payment/payment_success.html", context)
        elif payment_status == "cancel":
            payment.delete()
            return render(request, "games/payment/payment_cancel.html", context)

        return render(request, "games/payment/payment_error.html")

    def post(self, request, *args, **kwargs):
        game = get_object_or_404(Game, id=request.POST["game_id"])

        pid = uuid.uuid4().hex
        sid = settings.SID
        amount = game.price
        checksumstr = "pid=%s&sid=%s&amount=%s&token=%s" % (pid, sid, amount, settings.SID_KEY)
        checksum = hashlib.md5(checksumstr.encode("ascii")).hexdigest()

        values = {"pid": pid,
                  "sid": sid,
                  "success_url": settings.PAYMENT_SUCCESS_URL,
                  "cancel_url": settings.PAYMENT_CANCEL_URL,
                  "error_url": settings.PAYMENT_ERROR_URL,
                  "amount": amount,
                  "checksum": checksum}

        form = PaymentForm(initial=values)

        # Check for old payments that haven't been completed properly (either via /payment/success/ or payment/cancel/)
        try:
            old_payment = request.user.player.payments.get(game=game)
            if old_payment.completed:
                return render_to_response("games/payment/payment_error.html")
            old_payment.delete()
        except Payment.DoesNotExist:
            pass

        Payment.objects.values()

        payment = Payment(game=game, player=request.user.player, pid=pid)
        payment.save()
        return render(request, "games/payment/payment.html", {"game": game, "form": form})


def api_objects(request, api_version, collection, response_format, object_id=""):
    if api_version == "1":
        content_type, dump_content = api.response_formats[response_format]
        api_token = request.GET.get("api_token")

        try:
            offset = request.GET.get("offset") or 0
            limit = request.GET.get("limit") or 10
            offset = int(offset)
            limit = int(limit)
        except ValueError:
            response = dump_content({"detail": "Invalid value for offset and/or limit, should be integer"})
            return HttpResponse(response, content_type, status=400)

        try:
            user = WsdGamesUser.objects.get(api_token=api_token)
        except WsdGamesUser.DoesNotExist:
            user = AnonymousUser()

        model, serializer, check_owner, id_field_name = api.model_info[collection]
        if object_id == "":
            objs = model.objects.all()[offset:offset+limit]  # TODO: Bounds checks
            data = []
            for obj in objs:
                data.append(serializer(obj))
        else:
            obj = get_object_or_404(model, **{id_field_name: object_id})
            include_confidential = check_owner(obj, user)
            data = serializer(obj, include_confidential)

        response = dump_content(data)

        return HttpResponse(response, content_type=content_type)
    else:
        raise Http404
