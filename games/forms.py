from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from games.models import Player, Developer, Game


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(_("You must activate your account before logging in."), code="not_activated")


class WsdGamesUserCreationForm(forms.ModelForm):
    error_messages = {
        "duplicate_username": _("A user with that username already exists."),
        "duplicate_email": _("A user with that email already exists."),
        "password_mismatch": _("The two password fields didn't match."),
        }
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
                                help_text=_("Required. 30 characters or fewer. Letters, digits and "
                                            "@/./+/-/_ only."),
                                error_messages={
                                    "invalid": _("This value may contain only letters, numbers and "
                                                 "@/./+/-/_ characters.")})
    email = forms.EmailField(label=_("Email"), max_length=75,
                             help_text=_("Required. A valid email address."))
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            self.Meta.model._default_manager.get(username=username)
        except self.Meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages["duplicate_username"], code="duplicate_username")

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            self.Meta.model._default_manager.get(email=email)
        except self.Meta.model.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages["duplicate_email"], code="duplicate_email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages["password_mismatch"], code="password_mismatch")
        return password2

    def save(self, commit=True):
        user = super(WsdGamesUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = False
        if commit:
            user.save()
        return user


class PlayerSignupForm(WsdGamesUserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")

    def save(self, commit=True):
        user = super(PlayerSignupForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()

        player = Player(user=user)
        player.save()
        return user


class DeveloperSignupForm(WsdGamesUserCreationForm):
    name = forms.CharField(max_length=50, label="Company name")
    image_url = forms.URLField(required=False, label="Logo URL")
    description = forms.CharField(required=False, label="Company description")

    class Meta:
        model = get_user_model()
        fields = ("username", "name", "email", "image_url", "description")

    def save(self, commit=True):
        user = super(DeveloperSignupForm, self).save(commit=False)
        user.save()

        developer = Developer(user=user)
        developer.name = self.cleaned_data["name"]
        developer.image_url = self.cleaned_data["image_url"]
        developer.description = self.cleaned_data["description"]
        developer.save()
        return user

class GamePublishingForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ("name", "url", "image_url", "description", "categories", "price")


class PaymentForm(forms.Form):
    pid = forms.CharField(widget=forms.HiddenInput)
    sid = forms.CharField(widget=forms.HiddenInput)
    success_url = forms.URLField(widget=forms.HiddenInput)
    cancel_url = forms.URLField(widget=forms.HiddenInput)
    error_url = forms.URLField(widget=forms.HiddenInput)
    checksum = forms.CharField(widget=forms.HiddenInput)
    amount = forms.DecimalField(widget=forms.HiddenInput)


class UsernameForm(forms.Form):
    username_from_user = forms.RegexField(label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
                                          help_text=_("Required. 30 characters or fewer. Letters, digits and "
                                                      "@/./+/-/_ only."),
                                          error_messages={
                                              "invalid": _("This value may contain only letters, numbers and "
                                                           "@/./+/-/_ characters.")})

