from library.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def release_all(self):
        Occupation.objects.all().delete()
        seats = Seat.objects.all()

        for seat in seats:
            seat.status = 'VACANT'
            seat.save()


    def handle(self, *args, **options):
        self.release_all()

