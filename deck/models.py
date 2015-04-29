import random, string, datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from jsonfield import JSONField

def random_string():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))

class User(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['date_joined',]

    def __unicode__(self):
        return self.email

CARDS = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '0S', 'JS', 'QS', 'KS',
        'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '0D', 'JD', 'QD', 'KD',
        'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '0H', 'JH', 'QH', 'KH',
        'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '0C', 'JC', 'QC', 'KC']

class Deck(models.Model):
    key = models.CharField(default=random_string, max_length=15, db_index=True)
    last_used = models.DateTimeField(default=datetime.datetime.now)
    deck_count = models.IntegerField(default=1)
    stack = JSONField(null=True, blank=True)

    def shuffle(self):
        stack = []
        for i in range(0,self.deck_count):
            stack = stack+CARDS[:]
        random.shuffle(stack)
        self.stack = stack
        self.last_used = datetime.datetime.now()
        self.save()

def card_to_dict(card):
    value = card[:1]
    suit = card[1:]

    if value == 'A':
        value = 'ACE'
    elif value == 'J':
        value = 'JACK'
    elif value == 'Q':
        value = 'QUEEN'
    elif value == 'K':
        value = 'KING'
    elif value == '0':
        value = '10'

    if suit == 'S':
        suit = 'SPADES'
    elif suit == 'D':
        suit = 'DIAMONDS'
    elif suit == 'H':
        suit = 'HEARTS'
    elif suit == 'C':
        suit = 'CLUBS'

    d = {}

    d['value'] = value
    d['suit'] = suit
    d['image'] = 'http://deckofcardsapi.com/static/img/'+value+suit+'.png'

    return d