import datetime

from django.core.management.base import BaseCommand

from deck.models import Deck


class Command(BaseCommand):
    def handle(self, *args, **options):
        two_weeks_ago = datetime.datetime.now() - datetime.timedelta(days=14)
        decks = Deck.objects.filter(last_used__lt=two_weeks_ago)
        num = decks.count()
        decks.delete()
        print(str(num) + " decks deleted from db.")

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DELETE reltuples::bigint FROM pg_class WHERE relname = 'deck_deck';")
    row = cursor.fetchone()
    print("Approximate count:", row[0])



