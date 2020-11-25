from django.urls import path
from . import views
from .views import(

ProductHomeView,
ProductUpdateView,
ProductCreateView,
ProductDeleteView,
ProductsearchResultView,
)





urlpatterns = [
    path('products/', ProductHomeView.as_view(), name='product_home'),
    path('product/new/', ProductCreateView.as_view(),
         name='product_create'),
    path('Product/<int:pk>/update/',
         ProductUpdateView.as_view(), name='product_update'),
    path('Product/<int:pk>/delete/',
         ProductDeleteView.as_view(), name='product_delete'),
    path('products/product/search/',ProductsearchResultView.as_view(),name='product_search'),
]