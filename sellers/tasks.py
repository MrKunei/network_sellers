from random import randint
from celery import shared_task
from django.core.mail import EmailMessage, send_mail
from sellers.models import Seller


@shared_task
def add_debt_seller():
    sellers = Seller.objects.all()
    for seller in sellers:
        seller.debt += randint(5,500)
        seller.save()


@shared_task
def reduce_debt_seller():
    sellers = Seller.objects.all()
    for seller in sellers:
        reduce_sum = randint(100, 10000)
        if seller.debt <= reduce_sum:
            seller.debt = 0.00
        else:
            seller.debt -= reduce_sum
        seller.save()


@shared_task
def update_seller_debt(data):
    for d in data:
        seller = Seller.objects.get(id=d['pk'])
        seller.debt = 0.00
        seller.save()


@shared_task
def send_qr_email(email):
    mail = EmailMessage(
        subject='QR code',
        body='QR код контактных данных поставщика',
        from_email='',
        to=(email, ),
    )
    mail.attachments.append('media/qr/qr.png')
    mail.send(fail_silently=False)


