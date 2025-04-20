from django.contrib import admin
from .models import Base, InventoryItem, QrCode

admin.site.register(InventoryItem)
admin.site.register(Base)
admin.site.register(QrCode)