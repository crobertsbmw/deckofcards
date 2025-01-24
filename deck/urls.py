from django.urls import path, re_path
from deck import views

app_name = 'deck'  # added
urlpatterns = [
    # Deprecated URL Patterns (Consider removing if no longer needed)
    path('new/', views.new_deck, name='new_deck_d'),
    path('shuffle/', views.shuffle, name='shuffle_d'),
    path('shuffle/<slug:key>/', views.shuffle, name='shuffle_key_d'),
    path('draw/<slug:key>/', views.draw, name='draw_d'),

    # Current URL Patterns
    path('deck/new/', views.new_deck, name='new_deck'),
    path('deck/new/shuffle/', views.shuffle, name='shuffle'),
    path('deck/<slug:key>/shuffle/', views.shuffle, name='shuffle_key'),
    path('deck/new/draw/', views.draw, name='new_draw'),
    path('deck/<slug:key>/draw/', views.draw, name='draw'),
    path('deck/<slug:key>/', views.deck_info, name='info'),
    path('deck/<slug:key>/return/', views.return_to_deck, name='return'),

    path('deck/<slug:key>/pile/<slug:pile>/add/', views.add_to_pile, name='add'),
    path('deck/<slug:key>/pile/<slug:pile>/list/', views.list_cards_in_pile, name='list_pile'),
    path('deck/<slug:key>/pile/<slug:pile>/shuffle/', views.shuffle_pile, name='shuffle_pile'),
    path('deck/<slug:key>/pile/<slug:pile>/draw/', views.draw_from_pile, name='draw_pile'),
    path('deck/<slug:key>/pile/<slug:pile>/draw/<slug:location>/', views.draw_from_pile, name='draw_pile'),
    path('deck/<slug:key>/pile/<slug:pile>/return/', views.return_pile_to_deck, name='return'),   
]