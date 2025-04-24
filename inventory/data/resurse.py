from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *



class BaseInfoResource(resources.ModelResource):
    class Meta:
        model = BaseInfo




class InventoryItemResource(resources.ModelResource):
    class Meta:
        model = InventoryItem
        fields = ('id', 'objects_name', 'inventory_number', 'value', 'base', 'office', 'accountable_user')
        export_order = ('objects_name', 'inventory_number', 'value', 'base', 'office', 'accountable_user')