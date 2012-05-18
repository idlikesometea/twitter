from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^registro$', 'main.views.registro', name='registro'),
    url(r'^login$', 'main.views.log_in', name='login'),
    url(r'^done$', 'main.views.done', name='done'),
    url(r'^logout$', 'main.views.log_out', name='log_out'),
    url(r'^settings$', 'main.views.edit_profile', name='edit_profile'),
    url(r'^user/(?P<username>\w+)/$', 'main.views.show_user_profile', name='profile'),
    url(r'^tweet/(?P<id>\d+)/$', "main.views.view_tweet", name="tweet"),
    url(r'^follow/user/(?P<id>\d+)/$', "main.views.follow_user", name="follow_user"),
    url(r'^unfollow/user/(?P<id>\d+)/$', "main.views.unfollow_user", name="unfollow_user"),
    url(r'^tweet/add/$', 'main.views.add_tweet', name='add_tweet'),
    url(r'^timeline/$', 'main.views.feed', name='feed'),
    url(r'tweet/(?P<pk>\d+)/edit$', 'main.views.edit_tweet', name='edit_tweet'),
    url(r'^tweet/(?P<pk>\d+)/delete$', 'main.views.delete_tweet', name='delete_tweet'),
    url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset', name='reset'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    )
