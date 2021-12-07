import random
import string
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


def random_string():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))


class User(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['date_joined', ]

    def __unicode__(self):
        return self.email


CARDS = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '0S', 'JS', 'QS', 'KS',
         'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '0D', 'JD', 'QD', 'KD',
         'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '0C', 'JC', 'QC', 'KC',
         'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '0H', 'JH', 'QH', 'KH']
JOKERS = ['X1', 'X2']

SUITS = {'S': 'SPADES', 'D': 'DIAMONDS', 'H': 'HEARTS', 'C': 'CLUBS', '1': 'BLACK', '2': 'RED'}
VALUES = {'A': 'ACE', 'J': 'JACK', 'Q': 'QUEEN', 'K': 'KING', '0': '10', 'X': 'JOKER'}

class Deck(models.Model):
    key = models.CharField(default=random_string, max_length=15, db_index=True)
    last_used = models.DateTimeField(default=datetime.datetime.now)
    deck_count = models.IntegerField(default=1)
    stack = models.JSONField(null=True, blank=True) #The cards that haven't been drawn yet.
    piles = models.JSONField(null=True, blank=True) 
    deck_contents = models.JSONField(null=True, blank=True) #All the cards that should be included when shuffling and whatnot
    shuffled = models.BooleanField(default=False)
    include_jokers = models.BooleanField(default=False)
    
    def open_new(self, cards_used=None, jokers_enabled=False):
        self.include_jokers = False if jokers_enabled is None else jokers_enabled
        stack = []
        if cards_used is None: # use all the cards
            if self.deck_contents is None:
                cards = (CARDS, CARDS + JOKERS)[self.include_jokers]
            else:
                cards = self.deck_contents[:]
        else: # use a subset of a standard deck
            cards_used = cards_used.upper()
            # Only allow real cards
            valid_cards = (CARDS, CARDS + JOKERS)[self.include_jokers]
            cards = [x for x in cards_used.split(",") if x in valid_cards]
            self.deck_contents = cards[:]  # save the subset for future shuffles

        for i in range(0, self.deck_count):  # for loop over how many decks someone wants. Blackjack is usually 6.
            stack = stack + cards[:]  # adding the [:] forces the array to be copied.
        self.stack = stack
        self.last_used = datetime.datetime.now()
        self.save()

    def save(self, *args, **kwargs):
        self.last_used = datetime.datetime.now()
        super(Deck, self).save(*args, **kwargs)

def card_to_dict(card):
    value = card[:1]
    suit = card[1:]

    code = value + suit
    card_dict = {
        'code': code,
        'image': 'https://deckofcardsapi.com/static/img/%s.png' % code,
        'images': {
            'svg': 'https://deckofcardsapi.com/static/img/%s.svg' % code,
            'png': 'https://deckofcardsapi.com/static/img/%s.png' % code
        }
    }

    if code == 'AD':
        card_dict['image'] = 'https://deckofcardsapi.com/static/img/aceDiamonds.png'
        card_dict['images']['png'] = 'https://deckofcardsapi.com/static/img/aceDiamonds.png'
        card_dict['images']['svg'] = 'https://deckofcardsapi.com/static/img/aceDiamonds.svg'

    card_dict['value'] = VALUES.get(value) or value
    card_dict['suit'] = SUITS.get(suit) or suit
    return card_dict
