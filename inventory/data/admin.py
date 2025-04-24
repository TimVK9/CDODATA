from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resurse import *


admin.site.register(QrCode)




@admin.register(BaseInfo)
class BaseAdmin(ImportExportModelAdmin):
    resource_class = BaseInfoResource

@admin.register(InventoryItem)
class BaseAdmin(ImportExportModelAdmin):
    resource_class = InventoryItemResource
