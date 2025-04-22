from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *



class DivisionInfoResource(resources.ModelResource):
    class Meta:
        model = DivisionInfo



