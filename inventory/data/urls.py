from django.urls import path
from .views import (
     
    InventoryItemCreateView, InventoryList,
    InventoryItemUpdate, InventoryItemtDelete,


)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', InventoryList.as_view(), name='inventoryitem_list'),
    path('create/', InventoryItemCreateView.as_view(), name='inventoryitem_create'),
    path('update/<int:pk>', InventoryItemUpdate.as_view(), name='inventoryitem_update'),
    path('delete/<int:pk>', InventoryItemtDelete.as_view(), name='inventoryitem_delete'), 

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
