from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from games.views import *

urlpatterns = patterns('',
    url(r'^$', 'games.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login/username/([a-z0-9\-_]+)$', 'games.views.social_select_username', name='social_select_username'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'games.views.logout_view', name='logout'),
    url(r'^signup/(dev)?$', SignupView.as_view(), name="signup"),
    url(r'^publish-game/?$', GamePublishingView.as_view(), name="game_publishing"),

    url(r'^edit_profile$', login_required(EditProfileView.as_view()), name="edit_profile"),
    url(r'^profiles/([a-z0-9\-]+)$', 'games.views.profiles', name="profiles"),


    url(r'^payment/(success|cancel|error)?$', PaymentView.as_view(), name="payment"),

    url(r'^games/categories[/]?$', 'games.views.category_list', name='category_list'),
    url(r'^games/categories/([a-z0-9\-]+)$', 'games.views.category_detail', name='category_detail'),

    url(r'^games/developers[/]?$', 'games.views.developer_list', name='developer_list'),
    url(r'^games/developers/([a-z0-9\-]+)$', 'games.views.developer_detail', name='developer_detail'),

    url(r'^games/$', 'games.views.game_list', name='game_list'),
    url(r'^games/([a-z0-9\-]+)$', 'games.views.game_detail', name='game_detail'),

    url(r'^games/my_games[/]?$', 'games.views.my_games', name='my_games'),

    url(r'^api/v(?P<api_version>\d+)/(?P<collection>profiles|games|categories|developers).(?P<response_format>json)$',
        'games.views.api_objects'),
    url(r'^api/v(?P<api_version>\d+)/(?P<collection>profiles|games|categories|developers)/(?P<object_id>[a-z0-9\-]+).'
        r'(?P<response_format>json)$', 'games.views.api_objects'),
)
