import csv
from django.core.management.base import BaseCommand
from authentication.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):

        with open('data_db/user.csv', encoding='utf-8') as file:
            data = csv.DictReader(file)

            for d in data:
                user = User(
                    first_name=d['first_name'],
                    last_name=d['last_name'],
                    username=d['username'],
                    email = d['email']
                )
                user.set_password(d['password'])
                user.save()
