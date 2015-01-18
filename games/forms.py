from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from games.models import Player


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=75)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        player = Player()
        player.user_profile = user
        if commit:
            user.save()
            player.save()
        return user


class PaymentForm(forms.Form):
    pid = forms.CharField(widget=forms.HiddenInput)
    sid = forms.CharField(widget=forms.HiddenInput)
    success_url = forms.URLField(widget=forms.HiddenInput)
    cancel_url = forms.URLField(widget=forms.HiddenInput)
    error_url = forms.URLField(widget=forms.HiddenInput)
    checksum = forms.CharField(widget=forms.HiddenInput)
    amount = forms.DecimalField(widget=forms.HiddenInput)

    def set_values(self, values):
        for key, value in values.items():
            self.fields[key].initial = value
