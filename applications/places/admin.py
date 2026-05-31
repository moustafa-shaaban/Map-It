from django.contrib import admin

from .models import Type, Tag, Place, Review


class TypeAdmin(admin.ModelAdmin):
    model = Type
    search_fields = ["name"]

class TagAdmin(admin.ModelAdmin):
    model = Tag
    search_fields = ["name"]


class PlaceAdmin(admin.ModelAdmin):
    model = Place
    list_display = ("name", "type", "latitude", "longitude", "created_at")
    list_filter = ("type", "tags", "verified")
    search_fields = ["name"]


admin.site.register(Type, TypeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Review)