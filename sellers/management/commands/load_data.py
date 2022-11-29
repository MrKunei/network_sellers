import csv
import random
from random import randint

from django.core.management.base import BaseCommand
from sellers.models import Product, Seller

class Command(BaseCommand):

    def handle(self, *args, **options):

        with open('data_db/products.csv', encoding='utf-8') as file:
            data = csv.DictReader(file)
            data_list = ['2020-05-28', '2019-03-15', '2021-06-08', '2015-10-18',
                             '2010-02-05', '2018-04-04', '2013-05-11', '2011-09-11']
            for d in data:
                product = Product(
                    title=d['title'],
                    name_model='ABC'+ str(randint(99,999)),
                    release_date=random.choice(data_list)
                )
                product.save()

        with open('data_db/supplier.csv', encoding='utf-8') as file:
            data = csv.DictReader(file)

            for d in data:
                seller = Seller(
                    name=d['name'],
                    email=d['email'],
                    country=d['country'],
                    city=d['city'],
                    address=d['address'],
                    employees_id=randint(1,9),
                    parent_id= d['parent_id'] if d['parent_id'] != '' else None
                )
                seller.save()


        with open('data_db/seller_products.csv', encoding='utf-8') as file:
            data = csv.DictReader(file)

            for d in data:
                seller = Seller.objects.get(pk=d['seller_id'])
                seller.products.add(Product.objects.get(pk=d['product_id']))
                seller.save()


