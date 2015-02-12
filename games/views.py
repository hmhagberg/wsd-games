import hashlib

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
from games.utils import set_query_params


"""
BASE VIEWS
"""


class GenericWsdFormView(FormView):
    """
    Generic view that can be used when a single form needs to be displayed. Designed to be used with
    'games/base_genericForm.html' template.

    In addition to what there normally is in FormView, the following attributes can be changed:
    - title: Title of the page
    - header: Header of the page
    - submit_button_text: Text of the submit button
    - success_message: Message that is displayed in a banner when form is submitted succesfully. If None nothing is
      displayed

    All attributes have getter methods if their content needs to be changed dynamically.
    """

    template_name = "games/base_genericForm.html"
    success_url = "/"

    title = ""
    header = ""
    submit_button_text = "Submit"
    success_message = None

    def get_title(self):
        return self.title

    def get_header(self):
        return self.header

    def get_submit_button_text(self):
        return self.submit_button_text

    def get_success_message(self):
        return self.success_message

    def get_context_data(self, **kwargs):
        context = super(GenericWsdFormView, self).get_context_data(**kwargs)
        context.update({"title": self.get_title(),
                        "header": self.get_header(),
                        "submit_button_text": self.get_submit_button_text()})
        return context

    def form_valid(self, form):
        form.save()
        if self.success_message is not None:
            messages.success(self.request, self.get_success_message())
        return super(GenericWsdFormView, self).form_valid(form)


"""
AUTH VIEWS
"""


class LoginView(FormView):
    """
    View for logging in.
    """

    template_name = "games/auth/base_login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            messages.warning(request, "You already are logged in.")
            return redirect("home")
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, "You have logged in.")
        return redirect(self.request.GET.get("next") or "home")


def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out")
    return redirect("home")


class SignupView(FormView):
    """
    View for handling signup.
    """

    template_name = "games/auth/base_signup.html"
    form_class = WsdGamesUserSignupForm

    def get_form_class(self):
        if self.kwargs["dev_signup"] is None:
            return PlayerSignupForm
        else:
            return DeveloperSignupForm

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context.update({"dev_signup": self.kwargs["dev_signup"]})
        return context

    def get(self, request, *args, **kwargs):
        """
        Display signup form. Player form is displayed by default but if dev_signup is set Developer form is displayed
        instead. If request contains parameter 'activation_key' instead of displaying any form the key is checked
        against any unactivated users. If match is found user is either activated or, if expired, prompted to
        register again.
        """

        if request.user.is_authenticated():
            messages.warning(request, "You already have an account.")
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
            return super(SignupView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        link = SignupView.send_activation_mail(user)
        messages.success(self.request, "An activation email has been sent to the address you gave. "
                                       "To complete the signup process click the activation link in the email.")
        messages.debug(self.request, "Activation link: %s" % link)
        return redirect("home")

    @staticmethod
    def send_activation_mail(user):
        """
        Create activation instance and send activation email to user.
        """
        activation = SignupActivation(user=user)
        activation.save()

        activation_link = "{domain}/signup?activation_key={key}".format(domain=settings.DOMAIN, key=activation.key)
        message = "Thank you for signing up, {username}\n" \
                  "To activate your account click the following link: {link}\n" \
                  "The link expires in {expires_in} hours".format(username=user.username, link=activation_link,
                                                                  expires_in=settings.ACTIVATION_EXPIRATION_HOURS)
        send_mail("WSD Games Account Activation", message, "noreply@wsd-games.fi", [user.email])
        return activation_link


class SocialSignupSelectUsernameView(GenericWsdFormView):
    """
    View for selecting username when user logs in for the first time using social login. View checks that session has
    'pipeline_ask_username' flag which is set in ask_usernam in auth pipeline. If the flag is not set user is
    redirected.
    """

    form_class = UsernameForm

    title = "Select username"
    header = "Select username"
    submit_button_text = "OK"

    def get(self, request, *args, **kwargs):
        if request.session.get("pipeline_ask_username") is not None:
            return super(SocialSignupSelectUsernameView, self).get(request, *args, **kwargs)
        else:
            return redirect("home")

    def post(self, request, *args, **kwargs):
        if request.session.get("pipeline_ask_username") is not None:
            return super(SocialSignupSelectUsernameView, self).post(request, *args, **kwargs)
        else:
            return redirect("home")

    def form_valid(self, form):
        response = redirect("social:complete", self.request.GET.get("backend"))
        response = set_query_params(response, username_from_user=form.cleaned_data["username_from_user"])
        return response


"""
PROFILE EDITING VIEWS
"""


class ChangePasswordView(GenericWsdFormView):
    """
    View for changing user's password.
    """

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
    """
    View for editing user's profile. Used for both players and developers.
    """

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


"""
GAME MANAGING VIEWS
"""


class EditGameView(GenericWsdFormView):
    form_class = GameEditForm
    success_message = "Changes to the game have been saved."

    title = "Edit game"
    header = "Edit game"
    submit_button_text = "Submit change"

    def get(self, request, *args, **kwargs):
        game = get_object_or_404(Game, slug=self.args[0])
        if not request.user.is_developer():
            messages.error(request, "You must be a developer to manage the game.")
            return redirect("home")
        elif game.developer != request.user.developer:
            messages.error(request, "You must be the developer of the game to manage the game.")
            return redirect("home")
        else:
            return super(EditGameView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        game = get_object_or_404(Game, slug=self.args[0])
        form = GameEditForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(game.get_absolute_url())
        else:
            return super(EditGameView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditGameView, self).get_form_kwargs()
        kwargs["instance"] = get_object_or_404(Game, slug=self.args[0])
        return kwargs


class GamePublishingView(GenericWsdFormView):
    """
    View for publishing games. Only developers are allowed to publish games.
    """

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


def unpublish_game_confirm(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    context = {'game': game}
    if not request.user.is_developer():
        messages.error(request, "You must log in as developer to manage games.")
        return redirect("home")
    elif game.developer != request.user.developer:
        messages.error(request, "You can not manage a game published by someone else.")
        return redirect("home")
    else:
        return render(request, 'games/base_gameRemovalConfirmation.html', context)


def unpublish_game(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    game_name = game.name
    if not request.user.is_developer():
        messages.error(request, "You must log in as developer to manage games.")
        return redirect("home")
    elif game.developer != request.user.developer:
        messages.error(request, "You can not manage a game published by someone else.")
        return redirect("home")
    else:
        game.delete()
        messages.success(request, game_name + " has been removed from the store.")
        return redirect("home")


"""
DISPLAY VIEWS
"""


def home(request):
    games = Game.objects.all()
    context = {"title": "Games", "games": games}
    return render(request, 'games/base_grid_gameCard.html', context)

def profiles(request, profile_slug):
    profile = get_object_or_404(Player, slug=profile_slug)
    context = {'profile': profile}

    return render(request, 'games/base_profile.html', context)


def my_games(request):
    games = request.user.player.games()
    context = {"games": games, "title": "My Games"}
    return render(request, "games/base_grid_gameCard.html", context)


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
    """
    View for game detail. Game saving and highscores are handled here.
    :param game_slug: Slug for game that should be shown
    """

    game = get_object_or_404(Game, slug=game_slug)
    ownership_status = "not_owned"
    ownership = None
    context = {"game": game}
    if request.user.is_authenticated():
        if request.user.is_player() and request.user.player.owns_game(game):
            ownership_status = "owned"
            ownership = request.user.player.ownerships.get(player=request.user.player, game=game)

            # Handle game messages
            if request.method == 'POST' and ownership:
                if request.POST['messageType'] == "SCORE":
                    ownership.set_new_score(int(request.POST['score']))
                elif request.POST['messageType'] == "SAVE":
                    ownership.save_game(int(request.POST["gameState[score]"]),
                                        ','.join(request.POST.getlist("gameState[playerItems][]")))

        elif request.user.is_developer() and game.developer == request.user.developer:
            ownership_status = "developer"
            context.update({'publish_date': game.publish_date,
                            'sales_count': game.get_sales_count(),
                            'sales_count_year': game.get_sales_count(8760),
                            'sales_count_month': game.get_sales_count(720),
                            'sales_count_week': game.get_sales_count(168),
                            'sales_count_day': game.get_sales_count(24),
                            'sales_count_hour': game.get_sales_count(1), })

    context.update({'ownership_status': ownership_status, 'ownership': ownership})
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


"""
PAYMENT VIEWS
"""


class PaymentView(View):
    """
    View for handling payments
    """


    def get(self, request, payment_status, *args, **kwargs):
        """
        It is assumed that only payment service makes GET requests to this view. If some of the required payment
        parameters (PID, REF or checksum) are missing user is simply redirected to home. Otherwise parameters are
        verified and, if valid, payment is completed according to payment status.

        """

        pid = request.GET.get("pid")
        ref = request.GET.get("ref")
        received_checksum = request.GET.get("checksum")
        if not (pid and ref and received_checksum):
            return redirect("home")
        payment = get_object_or_404(Payment, pid=pid)
        checksumstr = "pid=%s&ref=%s&token=%s" % (pid, ref, settings.SID_KEY)
        calculated_checksum = hashlib.md5(checksumstr.encode("ascii")).hexdigest()

        if payment.completed:
            messages.error(request, "This payment has already been completed.")
            return redirect("home")
        elif calculated_checksum == received_checksum:
            if payment_status == "success":
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

        messages.error(request, "Oops! Something went wrong while handling your payment. Please, try again! GET")
        return redirect("home")

    def post(self, request, *args, **kwargs):
        """
        POST requests generate a form with payment details for game specified in the request. Payment is associated
        with the authenticated user. The generated form should be submitted to the payment service (i.e. this view
        renders confirmation page and when user clicks submit the form generated in this view is submitted to payment
        service.)
        """
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

        Payment(game=game, player=request.user.player, pid=pid).save()
        return render(request, "games/base_payment.html", {"game": game, "form": form})


"""
API VIEWS
"""


def api_view(request, api_version, collection, response_format, object_id=""):
    """
    View for handling API requests. Supported query parameters are:
    - offset: Offset for returned object range
    - limit: Number of objects returned

    :param api_version: API version as "v<number>". Currently only v1 is supported.
    :param collection: Collection of objects to return/search from
    :param response_format: Response format. Currently only json is supported.
    :param object_id: ID of requested object. If empty respinse with objects from 'offset' to 'offset+limit' in
    collection are
    returned.
    """
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
            objs = model.objects.all()[offset:offset + limit]
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
