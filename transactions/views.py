# Create your views here.
from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin


from .models import Transaction,  Sale
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


# ======================TRANSACTIONS SECTION=============================#


class TransactionHomeView(ListView):
    model = Transaction
    template_name = 'transactions/transactionshome.html'
    context_object_name = 'transactions'
    ordering = ['-transaction_date']


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'transactions/transactions_form.html'
    fields = [
        'clients_name',

        'id_number',
        'phone',
        'physical_address',
        'amount_applied',
        'security_offered',
        'repayment_day',
        'amount_payable',
        'repayment',
        'loan_status',


        'loan_disbursed',
        'loan_repaid',


    ]

    def form_valid(self, form):
        form.instance.lender = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin,  UpdateView):
    model = Transaction
    template_name = 'transactions/transactions_form.html'
    fields = [
        'clients_name',

        'id_number',
        'phone',
        'physical_address',
        'amount_applied',
        'security_offered',
        'repayment_day',
        'amount_payable',
        'repayment',
        'loan_status',
        'loan_disbursed',
        'loan_repaid',



    ]
    # form verification

    def form_valid(self, form):
        form.instance.lender = self.request.user
        return super().form_valid(form)


class TransactionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView,):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    context_object_name = 'transaction'
    success_url = reverse_lazy('transaction_home')
    permission_required = ('transactions.can_delete')


class SearchResultView(ListView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'transactions/transactionshome.html'

    def get_queryset(self):

        query = self.request.GET.get('q')
        object_list = Transaction.objects.filter(Q(id_number__icontains=query) | Q(
            repayment_day__icontains=query) | Q(loan_status__icontains=query))
        return object_list


# =========================SALES SECTION========================#


class SaleHomeView(ListView):
    model = Sale
    template_name = 'transactions/sales_home.html'
    context_object_name = 'sales'


class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    template_name = 'transactions/sales_form.html'
    fields = [
        'todays_sale',
        'sales_day',
        'cash_in_hand',
        'cylinder_sales',
        'electronics_and_accessories_sales',
        'loans_repaid',
        'loans_disbursed',

    ]

    def form_valid(self, form):
        form.instance.lender = self.request.user
        return super().form_valid(form)


class SaleUpdateView(LoginRequiredMixin,  UpdateView):
    model = Sale
    template_name = 'transactions/sales_form.html'
    fields = [
        'todays_sale',
        'sales_day',
        'cash_in_hand',
        'cylinder_sales',
        'electronics_and_accessories_sales',
        'loans_repaid',
        'loans_disbursed',

    ]
    # form verification

    def form_valid(self, form):
        form.instance.lender = self.request.user
        return super().form_valid(form)


class SaleDeleteView(LoginRequiredMixin, PermissionRequiredMixin,  DeleteView):
    model = Sale
    template_name = 'transactions/sales_delete.html'
    context_object_name = 'sale'
    success_url = reverse_lazy('sales_home')
    permission_required = ('sales.can_delete')


class SalesearchResultView(ListView):
    model = Sale
    context_object_name = 'sale'
    template_name = 'transactions/sales_home.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Sale.objects.filter(
            Q(sales_day__icontains=query) | Q(transaction_date__icontains=query))
        return object_list
