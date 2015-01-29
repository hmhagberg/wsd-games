from django.conf.urls import patterns, include, url
from django.contrib import admin

from games.views import PaymentView, SignupView, LoginView

urlpatterns = patterns('',
    url(r'^$', 'games.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login/username/([a-z0-9\-_]+)$', 'games.views.social_select_username', name='social_select_username'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'games.views.logout_view', name='logout'),
    url(r'^signup/(dev)?$', SignupView.as_view(), name="signup"),
    url(r'^signup/activate/([a-z0-9]+)$', 'games.views.signup_activation', name='signup_activation'),

    url(r'^profiles/([a-z0-9\-]+)$', 'games.views.profiles'),

    url(r'^payment/(success|cancel|error)?$', PaymentView.as_view(), name="payment"),

    url(r'^games/categories[/]?$', 'games.views.categories_list'),  # FIXME: HACK [/]?
    url(r'^games/categories/([a-z0-9\-]+)$', 'games.views.category'),

    url(r'^games/developers[/]?$', 'games.views.developers_list'),
    url(r'^games/developers/([a-z0-9\-]+)$', 'games.views.developer'),

    url(r'^games/$', 'games.views.games_list'),
    url(r'^games/([a-z0-9\-]+)$', 'games.views.game'),

    url(r'^games/my_games[/]?$', 'games.views.my_games'),

    url(r'^api/v(\d+)/profiles/([a-z0-9\-]*)$', 'games.views.api_profiles'),
    url(r'^api/v(\d+)/games/([a-z0-9\-]*)$', 'games.views.api_games'),
    url(r'^api/v(\d+)/games/categories/([a-z0-9\-]*)$', 'games.views.api_categories'),
    url(r'^api/v(\d+)/games/developers/([a-z0-9\-]*)$', 'games.views.api_developers'),
)
