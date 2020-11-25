
from django.contrib import admin
from django.urls import path, include
from . import settings
from transactions.views import TransactionHomeView

from django.conf.urls.static import static

urlpatterns = [
    path('root/', admin.site.urls, name='manager'),
    path('', TransactionHomeView.as_view(), name='transaction_home'),
    path('', include('pwa.urls')),

    path('transactions/', include('transactions.urls')),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
