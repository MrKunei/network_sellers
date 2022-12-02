import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_sellers.settings')

app = Celery('network_sellers')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'add-every-three-hours': {
        'task': 'sellers.tasks.add_debt_seller',
        'schedule': crontab(hour='*/3', minute=0),
    },
    'reduce-every-day': {
        'task': 'sellers.tasks.reduce_debt_seller',
        'schedule': crontab(hour=6, minute=30),
    },
}


# для тестирования
# app.conf.beat_schedule = {
#     'add-every-three-hours': {
#         'task': 'sellers.tasks.add_debt_seller',
#         'schedule': crontab(minute='*/1'),
#     },
#     'reduce-every-day': {
#         'task': 'sellers.tasks.reduce_debt_seller',
#         'schedule': crontab(minute='*/10'),
#     },
# }

