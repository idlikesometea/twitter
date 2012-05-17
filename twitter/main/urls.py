from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('main.views',
    url(r'^$', 'home', name='home'),
    url(r'^registro$', 'registro', name='registro'),
    url(r'^login$', 'log_in', name='login'),
    url(r'^done$', 'done', name='done'),
    url(r'^logout$', 'log_out', name='log_out'),
    url(r'^settings$', 'edit_profile', name='edit_profile'),
    url(r'^user/(?P<username>\w+)/$', 'show_user_profile', name='profile'),
    url(r'^tweet/(?P<id>\d+)/$', "view_tweet", name="tweet"),
    url(r'^follow/user/(?P<id>\d+)/$', "follow_user", name="follow_user"),
    url(r'^unfollow/user/(?P<id>\d+)/$', "unfollow_user", name="unfollow_user"),
    url(r'^tweet/add/$', 'add_tweet', name='add_tweet'),
    # url(r'^timeline', 'feed', name='feed'),
    )
