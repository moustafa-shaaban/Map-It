from django.contrib import admin

from django.db.models import Q

from .models import Type, Tag, Place


class RatingFilter(admin.SimpleListFilter):
    title = "rating"
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return [
            ("1", "★ 1+"),
            ("2", "★ 2+"),
            ("3", "★ 3+"),
            ("4", "★ 4+"),
            ("5", "★ 5"),
        ]

    def queryset(self, request, queryset):
        if self.value():
            value = int(self.value())
            return queryset.filter(
                rating__gte=value,
                rating__lt=value + 1
            )
        return queryset

class TypeAdmin(admin.ModelAdmin):
    model = Type
    search_fields = ["name"]

class TagAdmin(admin.ModelAdmin):
    model = Tag
    search_fields = ["name"]


class PlaceAdmin(admin.ModelAdmin):
    model = Place
    list_display = ("name", "type", "rating", "review_count", "latitude", "longitude", "created_at")
    list_filter = ("type", "tags", RatingFilter, "verified")
    search_fields = ["name"]


admin.site.register(Type, TypeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Place, PlaceAdmin)