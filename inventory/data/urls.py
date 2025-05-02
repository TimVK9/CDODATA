from django.urls import path
from .views import (
    BaseInfoListView, BaseInfoDetailView, BaseInfoCreateView,
    BaseInfoUpdateView, BaseInfoDeleteView,
    InventoryItemListView, InventoryItemDetailView,
    InventoryItemCreateView, InventoryItemUpdateView,
    InventoryItemDeleteView, import_inventory,
    download_template, ExportBaseInfoExcel

    
)

urlpatterns = [
    # BaseInfo URLs
    path('bases/', BaseInfoListView.as_view(), name='baseinfo-list'),
    path('bases/<int:pk>/', BaseInfoDetailView.as_view(), name='baseinfo-detail'),
    path('bases/create/', BaseInfoCreateView.as_view(), name='baseinfo-create'),
    path('bases/<int:pk>/update/', BaseInfoUpdateView.as_view(), name='baseinfo-update'),
    path('bases/<int:pk>/delete/', BaseInfoDeleteView.as_view(), name='baseinfo-delete'),
    
    # InventoryItem URLs
    path('', InventoryItemListView.as_view(), name='inventoryitem-list'),
    path('items/<int:pk>/', InventoryItemDetailView.as_view(), name='inventoryitem-detail'),
    path('items/create/', InventoryItemCreateView.as_view(), name='inventoryitem-create'),
    path('items/<int:pk>/update/', InventoryItemUpdateView.as_view(), name='inventoryitem-update'),
    path('items/<int:pk>/delete/', InventoryItemDeleteView.as_view(), name='inventoryitem-delete'),
    
    path('import-inventory/', import_inventory, name='import-inventory'),
    path('download-template/', download_template, name='download_template'),
    
    path('baseinfo/<int:pk>/export-excel/', ExportBaseInfoExcel.as_view(), name='export-baseinfo-excel'),


   
]