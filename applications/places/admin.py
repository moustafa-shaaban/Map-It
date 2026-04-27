from django.contrib import admin

from django.db.models import Q

from .models import Category, Tag, Place


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

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    search_fields = ["name"]

class TagAdmin(admin.ModelAdmin):
    model = Tag
    search_fields = ["name"]


class PlaceAdmin(admin.ModelAdmin):
    model = Place
    list_display = ("name", "category", "rating", "review_count", "latitude", "longitude")
    list_filter = ("category", "tags", RatingFilter, "verified")
    search_fields = ["name"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Place, PlaceAdmin)