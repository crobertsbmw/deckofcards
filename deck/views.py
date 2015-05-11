import json, random
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
    return new_deck(request, key, True)

def new_deck(request, key='', shuffle=False):
    deck_count = int(_get_request_var(request, 'deck_count'))
    if deck_count > 20:
        return HttpResponse(json.dumps({'success':False,'error':'The max number of Decks is 20.'}), content_type="application/json")
    if key:
        try:
            deck = Deck.objects.get(key=key)
        except Deck.DoesNotExist:
            return HttpResponse(json.dumps({'success':False,'error':'Deck ID does not exist.'}), content_type="application/json", status=404)
    else:
        deck = Deck()
        deck.deck_count = deck_count
    deck.open_new()
    if shuffle:
        random.shuffle(deck.stack)

    deck.save() #save the deck_count.
    resp = {'success':True, 'deck_id':deck.key, 'remaining':len(deck.stack)}
    return HttpResponse(json.dumps(resp), content_type="application/json")

def draw(request, key):
    success = True
    card_count = int(_get_request_var(request, 'count'))
    try:
        deck = Deck.objects.get(key=key)
    except Deck.DoesNotExist:
        return HttpResponse(json.dumps({'success':False,'error':'Deck ID does not exist.'}), content_type="application/json", status=404)

    if card_count > len(deck.stack):
        success = False
    cards = deck.stack[0:card_count]
    deck.stack = deck.stack[card_count:]
    deck.save() 

    a = []
    for card in cards:
        a.append(card_to_dict(card))
    if not success:
        resp = {'success':success, 'deck_id':deck.key, 'cards':a, 'remaining':len(deck.stack), 'error':'Not enough cards remaining to draw '+str(card_count)+' additional'}
    else:
        resp = {'success':success, 'deck_id':deck.key, 'cards':a, 'remaining':len(deck.stack)}

    return HttpResponse(json.dumps(resp), content_type="application/json")