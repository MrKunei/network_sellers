from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from authentication.models import User


def check_date_future(value: date):
    if value > date.today():
        raise ValidationError(f'{value} is in the future')


class Product(models.Model):
    title = models.CharField(max_length=25)
    name_model = models.CharField(max_length=50, null=True)
    release_date = models.DateField( validators=[check_date_future])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title


class Seller(MPTTModel):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    employees = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True,
            blank=True, related_name='children', verbose_name='supplier')
    debt = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=0.00)
    created = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name
