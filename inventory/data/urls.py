from django.urls import path
from .views import (
     
    CreateView, InventoryList,
    InventoryUpdate, InventoryItemtDelete,
    import_excel, ObjectDetail


)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', InventoryList.as_view(), name='inventoryitem_list'),
    path('create/', CreateView.as_view(), name='inventoryitem_create'),
    path('update/<int:pk>', InventoryUpdate.as_view(), name='update'),
    path('delete/<int:pk>', InventoryItemtDelete.as_view(), name='delete'), 
    path('import/', import_excel, name='import_excel'),
    path('detail/<int:pk>', ObjectDetail.as_view(), name='detail')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
