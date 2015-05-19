from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^new/$', 'deck.views.new_deck', name='new_deck_d'), #a week in and I am already deprecating things...
    url(r'^shuffle/$', 'deck.views.shuffle', name='shuffle_d'), #deprecated - May 18, 2015
    url(r'^shuffle/(?P<key>\w+)/$', 'deck.views.shuffle', name='shuffle_key_d'),#deprecated - May 18, 2015
    url(r'^draw/(?P<key>\w+)/$', 'deck.views.draw', name='draw_d'),#deprecated - May 18, 2015

    url(r'^deck/new/$', 'deck.views.new_deck', name='new_deck'),
    url(r'^deck/new/shuffle/$', 'deck.views.shuffle', name='shuffle'),
    url(r'^deck/(?P<key>\w+)/shuffle/$', 'deck.views.shuffle', name='shuffle_key'),
    url(r'^deck/(?P<key>\w+)/draw/$', 'deck.views.draw', name='draw'),

    url(r'^deck/(?P<key>\w+)/pile/(?P<pile>\w+)/add/$', 'deck.views.add_to_pile', name='add'),
    url(r'^deck/(?P<key>\w+)/pile/(?P<pile>\w+)/draw/$', 'deck.views.draw_from_pile', name='draw_pile'),
)