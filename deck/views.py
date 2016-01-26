import json, random, datetime
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect, HttpResponse, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from deck.models import User, Deck, card_to_dict

CARDS = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '0S', 'JS', 'QS', 'KS',
        'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '0D', 'JD', 'QD', 'KD',
        'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '0C', 'JC', 'QC', 'KC',
        'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '0H', 'JH', 'QH', 'KH']

def _get_request_var(request, key, default=1):
    if request.method == 'POST':
        return request.POST.get(key, default)
    else:
        return request.GET.get(key, default)

def shuffle(request, key=''):
    return new_deck(request, key, True)

def new_deck(request, key='', shuffle=False):
    #print(request.META['HTTP_ACCEPT'])
    deck_count = int(_get_request_var(request, 'deck_count'))
    deck_cards = _get_request_var(request, 'cards', None)
    if deck_count > 20:
        response = HttpResponse(json.dumps({'success':False,'error':'The max number of Decks is 20.'}), content_type="application/json")
        response['Access-Control-Allow-Origin'] = '*'
        return response
    if key:
        try:
            deck = Deck.objects.get(key=key)
        except Deck.DoesNotExist:
            response = HttpResponse(json.dumps({'success':False,'error':'Deck ID does not exist.'}), content_type="application/json", status=404)
            response['Access-Control-Allow-Origin'] = '*'
            return response
    else:
        deck = Deck()
        deck.deck_count = deck_count
    deck.open_new(deck_cards)
    shuffled = False
    if shuffle:
        random.shuffle(deck.stack)
        shuffled = True
    deck.save() #save the deck_count.

    resp = {'success':True, 'deck_id':deck.key, 'remaining':len(deck.stack), 'shuffled':shuffled}

    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def draw(request, key=None):
    success = True
    card_count = int(_get_request_var(request, 'count'))
    if not key:
        deck = Deck()
        deck.deck_count = int(_get_request_var(request, 'deck_count'))
        deck.open_new()
        random.shuffle(deck.stack)
        deck.save()
    else:
        try:
            deck = Deck.objects.get(key=key)
        except Deck.DoesNotExist:
            response = HttpResponse(json.dumps({'success':False,'error':'Deck ID does not exist.'}), content_type="application/json", status=404)
            response['Access-Control-Allow-Origin'] = '*'
            return response
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

    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response


def add_to_pile(request, key, pile):
    try:
        deck = Deck.objects.get(key=key)
    except Deck.DoesNotExist:
        return HttpResponse(json.dumps({'success':False,'error':'Deck ID does not exist.'}), content_type="application/json", status=404)

    cards = _get_request_var(request, 'cards', None)
    if cards is None:
        response = HttpResponse(json.dumps({'success':False,'error':'You must specify cards to add to the pile.'}), content_type="application/json", status=404)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        # Ignore case
        cards = cards.upper()
        # Only allow real cards
        cards = [x for x in cards.split(',') if x not in deck.stack and x in CARDS]

    if not deck.piles:
        deck.piles = {}
    for key in deck.piles: #iterate through all the piles and remove any specified cards from those piles.
        p = deck.piles[key] #times like these that I question if I should have just made piles a model instead of a json field...
        for card in cards: 
            if card in pile:
                p.remove(card)

    try: #try to add to the pile
        deck.piles[pile].extend(cards)
    except KeyError as e:#the pile is brand new
        deck.piles[pile] = cards #add the specified cards to the new pile
    deck.save()

    piles = {}
    for k in deck.piles:
        piles[k] = {"remaining":len(deck.piles[k])}

    resp = {'success':True, 'deck_id':deck.key, 'remaining':len(deck.stack), 'piles':piles}
    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def draw_from_pile(request, key, pile):
    try:
        deck = Deck.objects.get(key=key)
    except Deck.DoesNotExist:
        return HttpResponse(json.dumps({'success':False,'error':'Deck ID does not exist.'}), content_type="application/json", status=404)

    cards = _get_request_var(request, 'cards', None)
    cards_in_response = []

    p = deck.piles[pile] #times like these that I question if I should have just made piles a model instead of a json field...

    if cards:
        # Ignore case
        cards = cards.upper()
        # Only allow real cards
        cards = [x for x in cards.split(',') if x in CARDS]
   
        for card in cards:
            try:
                p.remove(card)
                cards_in_response.append(card)
            except:
                response = HttpResponse(json.dumps({'success':False,'error':'The pile, '+pile+\
                    ' does not contain the requested cards.'}), content_type="application/json", status=404)
                response['Access-Control-Allow-Origin'] = '*'
                return response
    else:
        card_count = int(_get_request_var(request, 'count'))
        if card_count > len(p):
            response = HttpResponse(json.dumps({'success':False,'error':'Not enough cards remaining to draw '+\
                str(card_count)+' additional'}), content_type="application/json", status=404)
            response['Access-Control-Allow-Origin'] = '*'
            return response

        cards_in_response = p[-card_count:]
        p = p[:-card_count]
    deck.piles[pile] = p
    deck.save()
    
    a = []

    for card in cards_in_response:
        a.append(card_to_dict(card))

    piles = {}
    for k in deck.piles:
        piles[k] = {"remaining":len(deck.piles[k])}

    resp = {'success':True, 'deck_id':deck.key, 'cards':a, 'piles':piles}
    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def clean_old_decks():
    two_weeks_ago = datetime.datetime.now() - datetime.timedelta(days=15)
    decks = Deck.objects.filter(last_used__lt=two_weeks_ago)
    num = decks.count()
    decks.delete()
    print(str(num) + " decks deleted from db.")
    #we only guarentee a deck for two weeks. But this funtion is only run manually from shell, whenever I feel to do it.
