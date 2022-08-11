from library.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def occupy_all(self):
        assert len(User.objects.all()) >= 16, 'There should be at least 16 users in the database'

        users = User.objects.all()
        seats = Seat.objects.all()

        for i in range(16):
            seat = Seat.objects.get(seatId=i+1)
            user = User.objects.all()[i]
            occ = Occupation(seat=seat, user=user)
            occ.save()

            seat.status = 'TAKEN'
            seat.save()
            


    def handle(self, *args, **options):
        self.occupy_all()

