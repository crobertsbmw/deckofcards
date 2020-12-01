import json
import random

from django.shortcuts import HttpResponse, render
from deck.models import Deck, card_to_dict, CARDS, JOKERS
from django.db import transaction

def doc_page(request):
    c = request.COOKIES.get('v', random.choice([1,2]))
    response = render(request, 'docs.html', {'v':int(c)})
    response.set_cookie("v", c)
    return response

def _get_request_var(request, key, default=1):
    if request.method == 'POST':
        return request.POST.get(key, default)
    else:
        return request.GET.get(key, default)

def get_jokers_enabled(request):
    j = _get_request_var(request, 'jokers_enabled')
    if isinstance(j, str):
        if j.lower() == 'true': return True
        if j.lower() == 'false': return False
    return

def shuffle(request, key=''):
    return new_deck(request, key, True)


def new_deck(request, key='', shuffle=False):
    deck_count = int(_get_request_var(request, 'deck_count'))
    deck_cards = _get_request_var(request, 'cards', None)
    jokers_enabled = get_jokers_enabled(request)
    if deck_count > 20:
        response = HttpResponse(
            json.dumps({'success': False, 'error': 'The max number of Decks is 20.'}),
            content_type="application/json"
        )
        response['Access-Control-Allow-Origin'] = '*'
        return response
    if key: #we are shuffling an existing deck
        print("we are here 1")
        try:
            deck = Deck.objects.get(key=key)
            deck.piles = {}
            if jokers_enabled is None:
                jokers_enabled = deck.include_jokers
        except Deck.DoesNotExist:
            print("we are here 3")
            return deck_id_does_not_exist()
    else: #creating a new deck
        deck = Deck()
        deck.deck_count = deck_count
    deck.open_new(deck_cards, jokers_enabled)
    deck.shuffled = False
    if shuffle:
        random.shuffle(deck.stack)
        deck.shuffled = True
    deck.save()  # save the deck_count.

    resp = {'success': True, 'deck_id': deck.key, 'remaining': len(deck.stack), 'shuffled': deck.shuffled}

    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response


def deck_info(request, key=0):
    try:
        deck = Deck.objects.get(key=key)
    except Deck.DoesNotExist:
        return deck_id_does_not_exist()

    resp = {'success': True, 'deck_id': deck.key, 'remaining': len(deck.stack), 'shuffled': deck.shuffled}
    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

@transaction.atomic
def draw(request, key=None):
    jokers_enabled = get_jokers_enabled(request)
    success = True
    card_count = int(_get_request_var(request, 'count'))
    if not key:
        deck = Deck()
        deck.deck_count = int(_get_request_var(request, 'deck_count'))
        deck.open_new(jokers_enabled=jokers_enabled)
        random.shuffle(deck.stack)
        deck.shuffled = True
        deck.save()
    else:
        try:
            deck = Deck.objects.get(key=key)
        except Deck.DoesNotExist:
            return deck_id_does_not_exist()
            
    if card_count > len(deck.stack):
        success = False
    cards = deck.stack[0:card_count]
    deck.stack = deck.stack[card_count:]
    deck.save()

    a = []
    for card in cards:
        a.append(card_to_dict(card))

    if not success:
        resp = {
            'success': success,
            'deck_id': deck.key,
            'cards': a,
            'remaining': len(deck.stack),
            'error': 'Not enough cards remaining to draw %s additional' % str(card_count)
        }
    else:
        resp = {'success': success, 'deck_id': deck.key, 'cards': a, 'remaining': len(deck.stack)}

    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response


def add_to_pile(request, key, pile):
    jokers_enabled = get_jokers_enabled(request)
    if not jokers_enabled: jokers_enabled = 0 #prevent a tuple indices error below.
    
    try:
        deck = Deck.objects.get(key=key)
    except Deck.DoesNotExist:
        return deck_id_does_not_exist()

    cards_specified = _get_request_var(request, 'cards', None)
    if cards_specified is None:
        response = HttpResponse(
            json.dumps({'success': False, 'error': 'You must specify cards to add to the pile.'}),
            content_type="application/json",
            status=404
        )
        response['Access-Control-Allow-Origin'] = '*'
        return response
    
    cards_specified = cards_specified.upper()
    # Only allow real cards

    all_cards = (CARDS, CARDS + JOKERS)[jokers_enabled]
    cards_specified = [x for x in cards_specified.split(',') if x not in deck.stack and x in all_cards]  # check that the cards has been drawn and is a valid card code.

    if not deck.piles:
        deck.piles = {}

    print(deck.piles)
    for key in deck.piles:  # iterate through all the piles and remove any specified cards from those piles.
        p = deck.piles[key]  # times like these that I question if I should have just made piles a model instead of a json field...
        for card in cards_specified: 
            if card in p:
                p.remove(card)

    try:  # try to add to the pile
        deck.piles[pile].extend(cards_specified)
    except KeyError as e:  # the pile is brand new
        deck.piles[pile] = cards_specified  # add the specified cards to the new pile
    deck.save()

    piles = {}
    for k in deck.piles:
        piles[k] = {'remaining': len(deck.piles[k])}

    resp = {'success': True, 'deck_id': deck.key, 'remaining': len(deck.stack), 'piles': piles}
    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response


def deck_id_does_not_exist():
    response = HttpResponse(
        json.dumps({'success': False, 'error': 'Deck ID does not exist.'}),
        content_type="application/json",
        status=404
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def shuffle_pile(request, key, pile):
    try:
        deck = Deck.objects.get(key=key)
    except Deck.DoesNotExist:
        return deck_id_does_not_exist()

    piles = {}
    random.shuffle(deck.piles[pile])
    deck.save()

    for k in deck.piles:  # iterate through all the piles and get the count.
        r = len(deck.piles[k])
        piles[k] = {"remaining": r}

    resp = {'success': True, 'deck_id': deck.key, 'remaining': len(deck.stack), 'piles': piles}
    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response


def list_cards_in_pile(request, key, pile):
    try:
        deck = Deck.objects.get(key=key)
    except Deck.DoesNotExist:
        return deck_id_does_not_exist()

    piles = {}

    for k in deck.piles:  # iterate through all the piles and list cards for specified pile.
        r = len(deck.piles[k])
        if k != pile:
            piles[k] = {"remaining": r}
        else:
            a = []
            for card in deck.piles[k]:
                a.append(card_to_dict(card))
            piles[k] = {"remaining": r, "cards": a}

    resp = {'success': True, 'deck_id': deck.key, 'remaining': len(deck.stack), 'piles': piles}
    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response


def draw_from_pile(request, key, pile, bottom=""):
    jokers_enabled = get_jokers_enabled(request)
    try:
        deck = Deck.objects.get(key=key)
    except Deck.DoesNotExist:
        return deck_id_does_not_exist()

    cards = _get_request_var(request, 'cards', None)
    cards_in_response = []

    p = deck.piles[pile]  # times like these that I question if I should have just made piles a model instead of a json field...

    if cards:
        # Ignore case
        cards = cards.upper()
        # Only allow real cards
        cards = [x for x in cards.split(',') if x in CARDS+JOKERS]
   
        for card in cards:
            try:
                p.remove(card)
                cards_in_response.append(card)
            except:
                response = HttpResponse(
                    json.dumps({
                        'success': False, 'error': 'The pile, %s does not contain the requested cards.' % pile
                    }),
                    content_type="application/json",
                    status=404
                )
                response['Access-Control-Allow-Origin'] = '*'
                return response
    else:
        card_count = int(_get_request_var(request, 'count'))
        if card_count > len(p):
            response = HttpResponse(
                json.dumps({
                    'success': False, 'error': 'Not enough cards remaining to draw %s additional' % str(card_count)
                }),
                content_type="application/json",
                status=404
            )
            response['Access-Control-Allow-Origin'] = '*'
            return response

        if bottom.lower() == "bottom":  # draw from the bottom of the pile
            cards_in_response = p[0:card_count]
            p = p[card_count:len(p)]
        else:  # draw cards from the top of the pile
            cards_in_response = p[-card_count:]
            p = p[:-card_count]

    deck.piles[pile] = p
    deck.save()
    
    a = []

    for card in cards_in_response:
        a.append(card_to_dict(card))

    piles = {}
    for k in deck.piles:
        piles[k] = {"remaining": len(deck.piles[k])}

    resp = {'success': True, 'deck_id': deck.key, 'cards': a, 'piles': piles}
    response = HttpResponse(json.dumps(resp), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response
