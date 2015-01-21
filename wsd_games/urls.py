from django.conf.urls import patterns, include, url
from django.contrib import admin

from games.views import PaymentView, SignupView

urlpatterns = patterns('',
    url(r'^$', 'games.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'games/auth/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'games/auth/logout.html'}, name='logout'),
    url(r'^signup/$', SignupView.as_view(), name="signup"),

    # FIXME: Currently /payment/successcancelerror and its variants are accepted
    url(r'^payment/(success)?(cancel)?(error)?$', PaymentView.as_view(), name="payment"),

    url(r'^games/categories[/]?$', 'games.views.categories_list'),  # FIXME: HACK [/]?
    url(r'^games/categories/([a-z0-9\-]+)$', 'games.views.category'),

    url(r'^games/developers[/]?$', 'games.views.developers_list'),
    url(r'^games/developers/([a-z0-9\-]+)$', 'games.views.developer'),

    url(r'^games/$', 'games.views.games_list'),
    url(r'^games/([a-z0-9\-]+)$', 'games.views.game'),
)
