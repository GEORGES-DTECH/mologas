# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

import calendar


class Stock(models.Model):
    CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('reset', 'reset')
    )

    DAYS = (
        ('monday', 'monday'),
        ('tuesday', 'tuesday'),
        ('wednesday', 'wednesday'),
        ('thursday', 'thursday'),
        ('friday', 'friday'),
        ('saturday', 'saturday'),
        ('sunday', 'sunday'),
        ('reset', 'reset'),
    )

    sales_day = models.CharField(max_length=100, choices=DAYS)
    is_it_for_loan = models.CharField(max_length=30, choices=CHOICES)

    product_name = models.CharField(max_length=200)
    sales_amount = models.IntegerField(default=0)
    product_quantity = models.IntegerField(default=1)
    product_price = models.IntegerField(default=0)
    product_quantity_sold = models.IntegerField(default=0)
    lender = models.ForeignKey(User, on_delete=models.PROTECT)
    transaction_date = models.DateTimeField('date published', auto_now=True)

    def __str__(self):
        return self.product_name

    # =======absolute urls================#
    def get_absolute_url(self):
        return reverse('product_home')

    @property
    def actual_price(self):
        return self.product_quantity_sold * self.product_price

    @property
    def remaining_stock(self):
        return self.product_quantity - self.product_quantity_sold

    @property
    def sales_today_total(self):
        method = Stock.objects.aggregate(total=Sum('sales_amount'))
        return method['total']
