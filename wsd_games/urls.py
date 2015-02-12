from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from games.views import *

urlpatterns = patterns('',
    url(r'^$', 'games.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login/select_username[/]?$', SocialSignupSelectUsernameView.as_view(), name='social_select_username'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'games.views.logout_view', name='logout'),
    url(r'^signup/(?P<dev_signup>dev)?$', SignupView.as_view(), name="signup"),
    url(r'^publish-game/?$', login_required(GamePublishingView.as_view()), name="game_publishing"),


    url(r'^edit_profile$', login_required(EditProfileView.as_view()), name="edit_profile"),
    url(r'^change_password$', login_required(ChangePasswordView.as_view()), name="change_password"),
    url(r'^profiles/([a-zA-Z0-9.@+-_]+)$', 'games.views.profiles', name="profiles"),


    url(r'^payment/(success|cancel|error)?$', PaymentView.as_view(), name="payment"),

    url(r'^categories[/]?$', 'games.views.category_list', name='category_list'),
    url(r'^categories/([a-z0-9\-]+)$', 'games.views.category_detail', name='category_detail'),

    url(r'^developers[/]?$', 'games.views.developer_list', name='developer_list'),
    url(r'^developers/([a-z0-9\-]+)$', 'games.views.developer_detail', name='developer_detail'),
    
    url(r'^edit_game/([a-z0-9\-]+)$', login_required(EditGameView.as_view()), name='edit_game'),
    url(r'^unpublish_game_confirm/([a-z0-9\-]+)$', 'games.views.unpublish_game_confirm', name='unpublish_game_confirm'),
    url(r'^unpublish_game/([a-z0-9\-]+)$', 'games.views.unpublish_game', name='unpublish_game'),

    url(r'^games/$', 'games.views.game_list', name='game_list'),

    url(r'^games/([a-z0-9\-]+)$', 'games.views.game_detail', name='game_detail'),


    url(r'^my_games[/]?$', 'games.views.my_games', name='my_games'),

    url(r'^api/v(?P<api_version>\d+)/(?P<collection>profiles|games|categories|developers).(?P<response_format>json)$',
        'games.views.api_objects'),
    url(r'^api/v(?P<api_version>\d+)/(?P<collection>profiles|games|categories|developers)/(?P<object_id>[a-z0-9\-]+).'
        r'(?P<response_format>json)$', 'games.views.api_objects'),
)
