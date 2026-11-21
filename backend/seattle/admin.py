from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Hospital, School, Library
from .resources import HospitalResource, SchoolResource, LibraryResource


class HospitalAdmin(ImportExportModelAdmin):
    resource_class = HospitalResource
    list_display = ("facility", "address", "latitude", "longitude")
    search_fields = ["facility", "address"]


class SchoolAdmin(ImportExportModelAdmin):
    resource_class = SchoolResource
    list_display = ("name", "address", "latitude", "longitude")
    search_fields = ["name", "address"]

class LibraryAdmin(ImportExportModelAdmin):
    resource_class = LibraryResource
    list_display = ("name", "address", "latitude", "longitude")
    search_fields = ["name", "address"]


admin.site.register(Hospital, HospitalAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Library, LibraryAdmin)
