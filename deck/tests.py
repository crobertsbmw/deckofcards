__author__ = "Chase Roberts"
__maintainers__ = ["Chase Roberts"]

import json

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import authenticate

from deck.views import *
from deck.models import *

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

        request = self.request_factory.get("/", {"count":10})
        response = draw(request, deck_id)
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['success'], True)
        self.assertEqual(resp['remaining'], 42)
        self.assertEqual(len(resp['cards']), 10)
        cards = resp['cards']

        card0 = cards[0]
        card1 = cards[1]

        request = self.request_factory.get("/", {"cards":card0['code']+','+card1['code']})
        response = add_to_pile(request, deck_id, 'chase')
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content.decode('utf-8'))
        self.assertEqual(resp['success'], True)
        self.assertEqual(resp['remaining'], 42)
        piles = resp['piles']
        self.assertEqual(piles['chase']['remaining'], 2)
        
        request = self.request_factory.get("/", {"cards":card0['code']})
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
