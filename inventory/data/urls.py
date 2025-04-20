from django.urls import path
from .views import (
    InventoryItemListView, 
    InventoryItemCreateView, 

)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', InventoryItemListView.as_view(), name='inventoryitem_list'),
    path('create/', InventoryItemCreateView.as_view(), name='inventoryitem_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
