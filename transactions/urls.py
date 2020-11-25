from django.urls import path

from . import views
from .views import (
    TransactionHomeView,
    TransactionUpdateView,
    TransactionCreateView,
    TransactionDeleteView,
    SearchResultView,






    SaleHomeView,
    SaleUpdateView,
    SaleCreateView,
    SaleDeleteView,
    SalesearchResultView

)


urlpatterns = [


    path('', TransactionHomeView.as_view(), name='transaction_home'),
    path('transaction/new/', TransactionCreateView.as_view(),
         name='transaction_create'),


    path('transaction/<int:pk>/update/',
         TransactionUpdateView.as_view(), name='transaction_update'),
    path('transaction/<int:pk>/delete/',
         TransactionDeleteView.as_view(), name='transaction_delete'),
    path('search/', SearchResultView.as_view(), name='search_results'),






    path('sales/', SaleHomeView.as_view(), name='sales_home'),
    path('sale/new/', SaleCreateView.as_view(),
         name='sales_create'),
    path('sale/<int:pk>/update/',
         SaleUpdateView.as_view(), name='sales_update'),
    path('sale/<int:pk>/delete/',
         SaleDeleteView.as_view(), name='sales_delete'),
    path('transactions/sale/search/',
         SalesearchResultView.as_view(), name='sale_search'),



]
