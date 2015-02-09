import hashlib

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse
from django.views.generic import View, FormView

from games import api
from games.models import *
from games.forms import *


def home(request):
    games = Game.objects.all()
    context = {"title": "Games", "games": games}
    return render(request, 'games/base_grid_gameCard.html', context)


class LoginView(FormView):
    template_name = "games/auth/base_login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("home")
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, "You have logged in")
        return redirect(self.request.GET.get("next") or "home")


class SignupView(View):

    def get(self, request, dev_signup, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("home")

        activation_key = request.GET.get("activation_key")
        if activation_key:
            confirmation = get_object_or_404(SignupActivation, key=activation_key)
            if confirmation.has_expired():
                confirmation.delete()
                messages.error(request, "This account activation confirmation has expired. You have to sign up again")
                return redirect("signup")
            else:
                confirmation.user.is_active = True
                confirmation.user.save()
                confirmation.delete()
                messages.success(request, "Congratulations! Your account has been activated. You can now log in.")
                return redirect("login")

        else:
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

        activation_link = "{domain}/signup?activation_key={key}".format(domain=settings.DOMAIN, key=activation.key)
        message = "Thank you for signing up, {username}\n" \
                  "To activate your account click the following link: {link}\n" \
                  "The link expires in {expires_in} hours".format(username=user.username, link=activation_link,
                                                                  expires_in=settings.ACTIVATION_EXPIRATION_HOURS)
        send_mail("WSD Games Account Activation", message, "noreply@wsd-games.fi", [user.email])
        return activation_link


class GenericWsdFormView(FormView):
    template_name = "games/base_generic_form.html"
    success_url = "/"
    success_message = None

    title = ""
    header = ""
    submit_button_text = "Submit"

    def get_title(self):
        return self.title

    def get_header(self):
        return self.header

    def get_submit_button_text(self):
        return self.submit_button_text

    def get_context_data(self, **kwargs):
        context = super(GenericWsdFormView, self).get_context_data(**kwargs)
        context.update({"title": self.get_title(),
                        "header": self.get_header(),
                        "submit_button_text": self.get_submit_button_text()})
        return context

    def form_valid(self, form):
        if self.success_message is not None:
            messages.success(self.request, self.success_message)
        return super(GenericWsdFormView, self).form_valid(form)


class GamePublishingView(GenericWsdFormView):
    form_class = GamePublishingForm
    success_message = "Your game has been published."

    title = "Publish game"
    header = "Publish game"
    submit_button_text = "Publish"

    def get(self, request, *args, **kwargs):
        if not request.user.is_developer():
            messages.error(request, "You must be developer to publish games")
            return redirect("home")
        else:
            return super(GamePublishingView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        game = form.save(commit=False)
        game.developer = self.request.user.developer
        game.save()
        messages.success(self.request, self.success_message)
        return redirect(game.get_absolute_url())


class ChangePasswordView(GenericWsdFormView):
    form_class = PasswordChangeForm
    success_message = "Your password has been changed."

    title = "Change password"
    submit_button_text = "Change password"

    def get_header(self):
        return self.request.user.username

    def get_form_kwargs(self):
        kwargs = super(ChangePasswordView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class EditProfileView(GenericWsdFormView):
    form_class = EditProfileForm
    success_message = "Changes to your profile have been saved."

    title = "Edit profile"
    submit_button_text = "Submit changes"

    def get_header(self):
        return self.request.user.username

    def get_form_kwargs(self):
        kwargs = super(EditProfileView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_form_class(self):
        if self.request.user.is_player():
            return PlayerEditProfileForm
        elif self.request.user.is_developer():
            return DeveloperEditProfileForm
        else:
            return EditProfileForm


def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out")
    return redirect("home")


def profiles(request, profile_slug):
    profile = get_object_or_404(Player, slug=profile_slug)
    context = {'profile': profile}

    return render(request, 'games/base_profile.html', context)


def my_games(request):
    games = request.user.player.games()
    context = {"games": games, "title": "My Games"}
    return render(request, "games/base_grid_gameCard.html", context)


def social_select_username(request, backend):
    """
    Username selection view for social auth
    """
    form = UsernameForm()
    return render(request, "games/auth/base_selectUsername.html", {"form": form, "backend": backend})


def game_list(request):
    return home(request)


def category_list(request):
    categories = Category.objects.all().order_by('name')
    context = {'categories': categories}
    return render(request, 'games/base_grid_categoryCard.html', context)


def developer_list(request):
    developers = Developer.objects.all().order_by('slug')
    context = {'developers': developers}
    return render(request, 'games/base_grid_developerCard.html', context)


def game_detail(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    ownership_status = "not_owned"
    ownership = None
    context = {"game": game}
    if request.user.is_authenticated():
        if hasattr(request.user, "player"):
            if request.user.player.owns_game(game):
                ownership_status = "owned"
                ownership = request.user.player.ownerships.get(player=request.user.player, game=game)
        elif game.developer == request.user.developer:
            ownership_status = "developer"
            context.update({'sales_count': game.get_sales_count()})

        context.update({'ownership_status': ownership_status, 'ownership': ownership})

    # Handle game messages
    if request.method == 'POST' and ownership:
        if request.POST['messageType'] == "SCORE":
            ownership.set_new_score(int(request.POST['score']))
        elif request.POST['messageType'] == "SAVE":
            ownership.save_game(int(request.POST["gameState[score]"]), ','.join(request.POST.getlist("gameState[playerItems][]")))

    return render(request, 'games/base_game.html', context)


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    games = category.games.all()
    context = {"title": category.name + " Games", "games": games}

    return render(request, "games/base_grid_gameCard.html", context)


def developer_detail(request, developers_slug):
    developer = get_object_or_404(Developer, slug=developers_slug)
    games = developer.games.all()
    context = {"title": "Games by " + developer.name, "games": games}
    return render(request, "games/base_grid_gameCard.html", context)


class PaymentView(View):

    def get(self, request, payment_status, *args, **kwargs):
        pid = request.GET.get("pid")
        ref = request.GET.get("ref")
        request_checksum = request.GET.get("checksum")
        if not (pid and ref and request_checksum):
            return redirect("home")
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
                messages.success(request, "Congratulations on you purchase!")
                return redirect(ownership.game.get_absolute_url())
        elif payment_status == "cancel":
            payment.delete()
            messages.info(request, "Your purchase has been cancelled.")
            return redirect("home")

        messages.error(request, "Oops! Something went wrong while handling your payment. Please, try again!")
        return redirect("home")

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
                messages.error(request, "Oops! Something went wrong while handling your payment. Please, try again!")
                return redirect("home")
            old_payment.delete()
        except Payment.DoesNotExist:
            pass

        Payment.objects.values()

        payment = Payment(game=game, player=request.user.player, pid=pid)
        payment.save()
        return render(request, "games/base_payment.html", {"game": game, "form": form})


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
            objs = model.objects.all()[offset:offset+limit]
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
