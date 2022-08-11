from library.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    
    def disp(self):
        print(User.objects.all())

    def handle(self, *args, **options):
        self.disp()

