import json
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect, HttpResponse, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from deck.models import User, Deck, card_to_dict

def _get_request_var(request, key):
    if request.method == 'POST':
        return request.POST.get(key, 1)
    else:
        return request.GET.get(key, 1)

def shuffle(request, key=''):
    deck_count = int(_get_request_var(request, 'deck_count'))
    if deck_count > 20:
        return HttpResponse(json.dumps({'success':False,'error':'The max number of Decks is 20.'}), content_type="application/json")
    if key:
        deck = Deck.objects.get(key=key)
    else:
        deck = Deck()
        deck.deck_count = deck_count
    deck.shuffle()
    resp = {'success':True, 'deck_id':deck.key, 'remaining':len(deck.stack)}
    return HttpResponse(json.dumps(resp), content_type="application/json")

def draw(request, key):
    card_count = int(_get_request_var(request, 'count'))
    deck = Deck.objects.get(key=key)
    cards = deck.stack[0:card_count]
    deck.stack = deck.stack[card_count:]
    deck.save() 

    a = []
    for card in cards:
        a.append(card_to_dict(card))

    resp = {'success':True, 'deck_id':deck.key, 'cards':a, 'remaining':len(deck.stack)}
    return HttpResponse(json.dumps(resp), content_type="application/json")