from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q


from .models import Stock
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ProductHomeView(ListView):
    model = Stock
    template_name = 'products/productshome.html'
    context_object_name = 'products'
    ordering = ['-transaction_date']


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    template_name = 'products/products_form.html'
    fields = [
        'product_name',
        'sales_day',
        # 'is_it_for_loan',
        'product_quantity',
        # 'product_price',
        'product_quantity_sold',
        # 'sales_amount'


    ]

    def form_valid(self, form):
        form.instance.lender = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin,  UpdateView):
    model = Stock
    template_name = 'products/products_form.html'
    fields = [
        'product_name',
        'sales_day',
        # 'is_it_for_loan',
        'product_quantity',
        # 'product_price',
        'product_quantity_sold',
        # 'sales_amount'

    ]
    # form verification

    def form_valid(self, form):
        form.instance.lender = self.request.user
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin,  DeleteView):
    model = Stock
    template_name = 'products/products_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_home')
    permission_required = ('products.can_delete')


class ProductsearchResultView(ListView):
    model = Stock
    context_object_name = 'product'
    template_name = 'products/productshome.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Stock.objects.filter(Q(product_name__icontains=query) | Q(transaction_date__icontains=query) |
                                           Q(sales_day__icontains=query))
        return object_list
