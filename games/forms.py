from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from games.models import Player, Developer, Game


name_regex = r"^[^\W\d_]+$"
username_regex = r"^[\w.@+-]+$"


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'not_activated': _("You must activate your account before logging in."),
        }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages["not_activated"], code="not_activated")

    def clean(self):
        try:
            super(LoginForm, self).clean()
        except forms.ValidationError as e:  # Attach error to password field rather than the form as a whole
            self.add_error("password", e)


class WsdGamesUserCreationForm(forms.ModelForm):
    error_messages = {
        "duplicate_username": _("A user with that username already exists."),
        "duplicate_email": _("A user with that email already exists."),
        "password_mismatch": _("The two password fields didn't match."),
        }
    username = forms.RegexField(label=_("Username"), max_length=30, regex=username_regex,
                                help_text=_("Required"),
                                error_messages={
                                    "invalid": _("This value may contain only letters, numbers and "
                                                 "@/./+/-/_ characters.")})
    email = forms.EmailField(label=_("Email"), max_length=75, help_text=_("Required"))
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
    first_name = forms.RegexField(label=_("First name"), max_length=50, regex=name_regex)
    last_name = forms.RegexField(label=_("Last name"), max_length=50, regex=name_regex)

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
    name = forms.RegexField(label=_("Company name"), min_length=1,  max_length=50, regex=name_regex)
    image_url = forms.URLField(label=_("Logo URL"), required=False)
    description = forms.CharField(label=_("Company description"), required=False)

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


class EditProfileForm(forms.Form):
    user_model = get_user_model()

    error_messages = {
        "duplicate_username": _("A user with that username already exists."),
        "duplicate_email": _("A user with that email already exists."),
        "password_mismatch": _("The two password fields didn't match."),
        }

    username = forms.RegexField(label=_("Username"), max_length=30, regex=username_regex,
                                error_messages={
                                    "invalid": _("This value may contain only letters, numbers and "
                                                 "@/./+/-/_ characters.")})
    email = forms.EmailField(label=_("Email"), max_length=75)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs["initial"] = kwargs.get("initial", {})
        kwargs["initial"].update({"username": self.user.username,
                                  "email": self.user.email})
        super(EditProfileForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            other = self.user_model._default_manager.get(username=username)
            if self.user.id == other.id:
                return username
        except self.user_model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages["duplicate_username"], code="duplicate_username")

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            other = self.user_model._default_manager.get(email=email)
            if self.user.id == other.id:
                return email
        except self.user_model.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages["duplicate_email"], code="duplicate_email")

    def save(self, commit=True):
        self.user.username = self.cleaned_data["username"]
        self.user.email = self.cleaned_data["email"]
        if commit:
            self.user.save()
        return self.user


class PlayerEditProfileForm(EditProfileForm):
    first_name = forms.RegexField(label=_("First name"), min_length=1,  max_length=50, regex=name_regex)
    last_name = forms.RegexField(label=_("Last name"), min_length=1, max_length=50, regex=name_regex)
    about_me = forms.CharField(label=_("About me"), required=False, widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs["initial"] = kwargs.get("initial", {})
        kwargs["initial"].update({"first_name": self.user.first_name,
                                  "last_name": self.user.last_name,
                                  "about_me": self.user.player.about_me})
        super(PlayerEditProfileForm, self).__init__(user, *args, **kwargs)

    def save(self, commit=True):
        super(PlayerEditProfileForm, self).save(commit=True)
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.player.about_me = self.cleaned_data["about_me"]
        if commit:
            self.user.save()
            self.user.player.save()
        return self.user


class DeveloperEditProfileForm(EditProfileForm):
    name = forms.RegexField(label=_("Company name"), max_length=50, regex=name_regex)
    image_url = forms.URLField(label=_("Logo URL"), required=False)
    description = forms.CharField(label=_("Company description"), required=False, widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs["initial"] = kwargs.get("initial", {})
        kwargs["initial"].update({"name": self.user.developer.name,
                                  "image_url": self.user.developer.image_url,
                                  "description": self.user.developer.description})
        super(DeveloperEditProfileForm, self).__init__(user, *args, **kwargs)

    def save(self, commit=True):
        super(DeveloperEditProfileForm, self).save(commit=True)

        self.user.developer.name = self.cleaned_data["name"]
        self.user.developer.image_url = self.cleaned_data["image_url"]
        self.user.developer.description = self.cleaned_data["description"]
        if commit:
            self.user.developer.save()
        return self.user


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
    user_model = get_user_model()

    username_from_user = forms.RegexField(label=_("Username"), max_length=30, regex=username_regex,
                                          error_messages={
                                          "invalid": _("This value may contain only letters, numbers and "
                                                       "@/./+/-/_ characters.")})

    def clean_username(self):
        username_from_user = self.cleaned_data["username"]
        try:
            other = self.user_model._default_manager.get(username=username_from_user)
            if self.user.id == other.id:
                return username_from_user
        except self.user_model.DoesNotExist:
            return username_from_user
        raise forms.ValidationError(self.error_messages["duplicate_username"], code="duplicate_username")

