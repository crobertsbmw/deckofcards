from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^new/$', 'deck.views.new_deck', name='new_deck'),
    url(r'^shuffle/$', 'deck.views.shuffle', name='shuffle'),
    url(r'^shuffle/(?P<key>\w+)/$', 'deck.views.shuffle', name='shuffle_key'),
    url(r'^draw/(?P<key>\w+)/$', 'deck.views.draw', name='draw'),
)