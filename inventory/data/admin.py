from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resurse import *


admin.site.register(InventoryItem)
admin.site.register(QrCode)




@admin.register(DivisionInfo)
class BaseAdmin(ImportExportModelAdmin):
    resource_class = DivisionInfoResource