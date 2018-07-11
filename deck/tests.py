__author__ = "Chase Roberts"
__maintainers__ = ["Chase Roberts"]

from django.test import TestCase
from django.test.client import RequestFactory

from deck.views import *


class DeckTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_flow(self):
        request = self.request_factory.get("/", {})
        response = new_deck(request)
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['success'], True)
        self.assertEqual(resp['shuffled'], False)
        deck_id = resp['deck_id']

        request = self.request_factory.get("/", {})
        response = draw(request, deck_id)
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['success'], True)
        ace = resp['cards'][0]
        self.assertEqual(ace['suit'], 'SPADES')
        self.assertEqual(ace['value'], 'ACE')
        self.assertEqual(ace['code'], 'AS')
        self.assertEqual(resp['remaining'], 51)

        request = self.request_factory.get("/", {})
        response = shuffle(request, deck_id)
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['success'], True)
        self.assertEqual(resp['shuffled'], True)
        self.assertEqual(resp['remaining'], 52)

        request = self.request_factory.get("/", {"count": 10})
        response = draw(request, deck_id)
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['success'], True)
        self.assertEqual(resp['remaining'], 42)
        self.assertEqual(len(resp['cards']), 10)
        cards = resp['cards']

        card0 = cards[0]
        card1 = cards[1]

        request = self.request_factory.get("/", {"cards": card0['code']+','+card1['code']})
        response = add_to_pile(request, deck_id, 'chase')
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['success'], True)
        self.assertEqual(resp['remaining'], 42)
        piles = resp['piles']
        self.assertEqual(piles['chase']['remaining'], 2)
        
        request = self.request_factory.get("/", {"cards": card0['code']})
        response = draw_from_pile(request, deck_id, 'chase')
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['success'], True)
        cards = resp['cards']
        self.assertEqual(cards[0]['code'], card0['code'])
        piles = resp['piles']
        self.assertEqual(piles['chase']['remaining'], 1)

        request = self.request_factory.get("/", {})
        response = draw_from_pile(request, deck_id, 'chase')
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))

        self.assertEqual(resp['success'], True)
        cards = resp['cards']
        self.assertEqual(cards[0]['code'], card1['code'])
        piles = resp['piles']
        self.assertEqual(piles['chase']['remaining'], 0)

    def test_partial_deck(self):
        # test to make sure a new partial deck is returned when requested
        request = self.request_factory.get("/", {'cards': 'AC,AD,AH,AS'})
        response = shuffle(request)
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['success'], True)
        self.assertEqual(resp['shuffled'], True)
        deck_id = resp['deck_id']
        self.assertEqual(resp['remaining'], 4)

        # draw 4 cards and make sure they match the input data (and verify deck is empty)
        request = self.request_factory.get("/", {'count': 4})
        response = draw(request, deck_id)
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['success'], True)
        one, two, three, four = False, False, False, False
        for card in resp['cards']:
            if card['code'] == 'AS':
                one = True
            elif card['code'] == 'AD':
                two = True
            elif card['code'] == 'AH':
                three = True
            elif card['code'] == 'AC':
                four = True
        self.assertEqual(resp['remaining'], 0)
        self.assertEqual(one, True)
        self.assertEqual(two, True)
        self.assertEqual(three, True)
        self.assertEqual(four, True)

        # verify that reshuffling a partial deck returns a partial deck
        request = self.request_factory.get("/", {'cards': 'KC,KD,KH,KS'})
        response = shuffle(request)
        resp = json.loads(response.content.decode('utf-8'))
        deck_id = resp['deck_id']
        reshuffle_request = self.request_factory.get("/", {})
        response = shuffle(reshuffle_request, deck_id)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['remaining'], 4)

    def test_draw_new(self):
        request = self.request_factory.get("/", {'count': 5})
        response = draw(request)
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['success'], True)
        self.assertEqual(resp['remaining'], 47)
