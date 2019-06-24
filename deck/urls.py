from django.conf.urls import url
from deck import views

app_name = 'deck'  # added

urlpatterns = [
    url(r'^new/$', views.new_deck, name='new_deck_d'),  # a week in and I am already deprecating things...
    url(r'^shuffle/$', views.shuffle, name='shuffle_d'),  # deprecated - May 18, 2015
    url(r'^shuffle/(?P<key>\w+)/$', views.shuffle, name='shuffle_key_d'),  # deprecated - May 18, 2015
    url(r'^draw/(?P<key>\w+)/$', views.draw, name='draw_d'),  # deprecated - May 18, 2015

    url(r'^deck/new/$', views.new_deck, name='new_deck'),
    url(r'^deck/new/shuffle/$', views.shuffle, name='shuffle'),
    url(r'^deck/(?P<key>\w+)/shuffle/$', views.shuffle, name='shuffle_key'),
    url(r'^deck/new/draw/$', views.draw, name='new_draw'),
    url(r'^deck/(?P<key>\w+)/draw/$', views.draw, name='draw'),
    url(r'^deck/(?P<key>\w+)/$', views.deck_info, name='info'),

    url(r'^deck/(?P<key>\w+)/pile/(?P<pile>\w+)/add/$', views.add_to_pile, name='add'),
    url(r'^deck/(?P<key>\w+)/pile/(?P<pile>\w+)/list/$', views.list_cards_in_pile, name='list_pile'),
    url(r'^deck/(?P<key>\w+)/pile/(?P<pile>\w+)/shuffle/$', views.shuffle_pile, name='shuffle_pile'),
    url(r'^deck/(?P<key>\w+)/pile/(?P<pile>\w+)/draw/$', views.draw_from_pile, name='draw_pile'),
    url(r'^deck/(?P<key>\w+)/pile/(?P<pile>\w+)/draw/(?P<bottom>\w+)/$', views.draw_from_pile, name='draw_pile'),
]
