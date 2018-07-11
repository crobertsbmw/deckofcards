import datetime

from django.core.management.base import BaseCommand

from deck.models import Deck


class Command(BaseCommand):
    def handle(self, *args, **options):
        two_weeks_ago = datetime.datetime.now() - datetime.timedelta(days=20)
        decks = Deck.objects.filter(last_used__lt=two_weeks_ago)
        num = decks.count()
        decks.delete()
        print(str(num) + " decks deleted from db.")
