# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.functional import cached_property
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from io import BytesIO
from PIL import Image
from django.core.files import File
import calendar

# ===========transactions=============================

'''
def compress(photo):
    im = Image.open(photo)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    new_photo = File(im_io, name=photo.name)
    return new_photo
'''


class Transaction(models.Model):
    CHOICES = (
        ('monday', 'monday'),
        ('tuesday', 'tuesday'),
        ('wednesday', 'wednesday'),
        ('thursday', 'thursday'),
        ('friday', 'friday'),
        ('saturday', 'saturday'),
        ('sunday', 'sunday'),
    )

    STATUS = (
        ('pending', 'pending'),
        ('cleared', 'cleared'),
        ('renew for the first time', 'renew for the first time'),
        ('renew for the second time', 'renew for the second time'),
        ('renew for the third time', 'renew for the third time'),
        ('renew for the fourth time', 'renew for the fourth time'),
        ('renew for the fifth time', 'renew for the fifth time'),

    )
    clients_name = models.CharField(max_length=200, blank=True)

    id_number = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    amount_applied = models.IntegerField(default=0)
    amount_payable = models.IntegerField(default=0)
    defaulted_days = models.IntegerField(default=0)
    repayment = models.IntegerField(default=0)
    loan_disbursed = models.IntegerField(default=0)
    loan_repaid = models.IntegerField(default=0)

    fines_charged = models.IntegerField(default=0)
    transaction_fines = models.IntegerField(default=0)
    repayment_day = models.CharField(max_length=10, choices=CHOICES)
    loan_status = models.CharField(
        max_length=30, choices=STATUS, default='pending')
    physical_address = models.CharField(max_length=50, blank=True)
    security_offered = models.CharField(max_length=200, blank=True)
    transaction_date = models.DateTimeField(default=timezone.now)
    lender = models.ForeignKey(User, on_delete=models.PROTECT)
    interest_rate = 0.3

    def __str__(self):
        return self.clients_name

    # =======absolute urls================#
    def get_absolute_url(self):
        return reverse('transaction_home')
    '''
    def save(self, *args, **kwargs):
        new_photo = compress(self.photo)
        self.photo = new_photo
        super().save(*args, **kwargs)
    '''
    @cached_property
    def interest_due(self):

        interest_charge = round(self.amount_applied *
                                self.interest_rate)+self.fines_charged
        return interest_charge

    @cached_property
    def loan_payable_amount(self):
        method = self.interest_due
        return method+self.amount_applied

    @cached_property
    def loan_balance_calculation(self):

        balance = self.amount_payable - self.repayment
        return balance

    @cached_property
    def due_weekly_date(self):
        if self.loan_status == "pending" or "cleared" or "renew first time" or "renew first time" \
                or "renew third time" or "renew fourth time" or "renew fifth time":
            date = self.transaction_date
            due_date = date + relativedelta(weeks=+1)
            return due_date

    @cached_property
    def fines_calculation(self):
        if self.fines_charged == 0:
            method = self.interest_due
            return round(method / 7 * self.defaulted_days)
        else:
            return self.fines_charged

    @cached_property
    def the_date_today(self):
        now = datetime.now()
        return now


#  =======================totals========================


    @cached_property
    def loans_disbursed_total(self):
        method = Transaction.objects.aggregate(total=Sum('loan_disbursed'))
        return method['total']

    @cached_property
    def loans_repaid_total(self):
        method = Transaction.objects.aggregate(total=Sum('loan_repaid'))
        return method['total']

    @cached_property
    def cash_today_total(self):
        method = self.loans_repaid_total
        method2 = self.loans_disbursed_total
        return method - method2

    @cached_property
    def fines_total(self):
        method = Transaction.objects.aggregate(total=Sum('fines_charged'))
        return method['total']

    @cached_property
    def interest_total(self):
        method1 = self.fines_total
        method2 = Transaction.objects.aggregate(total=Sum('amount_applied'))
        return round(method2['total'] * self.interest_rate) + method1

    @cached_property
    def loans_given_total(self):
        method2 = Transaction.objects.aggregate(total=Sum('amount_applied'))
        return method2['total']

    @cached_property
    def loans_payable_total(self):
        method1 = self.interest_total
        method2 = self.loans_given_total
        return method1+method2

    @cached_property
    def repayments_total(self):
        method2 = Transaction.objects.aggregate(total=Sum('repayment'))
        return method2['total']

    @cached_property
    def loan_balance_total(self):
        method1 = self.repayments_total
        method2 = Transaction.objects.aggregate(total=Sum('amount_payable'))
        return method2['total'] - method1


class Sale(models.Model):
    CHOICES = (
        ('monday', 'monday'),
        ('tuesday', 'tuesday'),
        ('wednesday', 'wednesday'),
        ('thursday', 'thursday'),
        ('friday', 'friday'),
        ('saturday', 'saturday'),
        ('sunday', 'sunday'),
    )
    sales_day = models.CharField(max_length=100, choices=CHOICES)
    todays_sale = models.CharField(max_length=200, default='add sales')
    cylinder_sales = models.IntegerField(default=0)
    cash_in_hand = models.IntegerField(default=0)
    electronics_and_accessories_sales = models.IntegerField(default=0)
    loans_disbursed = models.IntegerField(default=0)
    loans_repaid = models.IntegerField(default=0)
    transaction_date = models.DateTimeField('date published', auto_now=True)
    lender = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.todays_sale

    def get_absolute_url(self):
        return reverse('sales_home')

    def total_revenue(self):
        return self.cash_in_hand+self.cylinder_sales+self.electronics_and_accessories_sales+self.loans_repaid-self.loans_disbursed
