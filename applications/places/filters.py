# filters.py

import django_filters
from django import forms
from django.db.models import Q
from .models import Place, Tag


class PlaceFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Name contains",
    )

    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags",
        label="Tags",
        widget=forms.CheckboxSelectMultiple,
        queryset=Tag.objects.all()
    )

    rating_min = django_filters.NumberFilter(
        field_name="rating",
        lookup_expr="gte",
        label="Minimum rating",
    )
    rating_max = django_filters.NumberFilter(
        field_name="rating",
        lookup_expr="lte",
        label="Maximum rating",
    )

    review_count_min = django_filters.NumberFilter(
        field_name="review_count",
        lookup_expr="gte",
        label="Minimum review count",
    )
    review_count_max = django_filters.NumberFilter(
        field_name="review_count",
        lookup_expr="lte",
        label="Maximum review count",
    )

    verified = django_filters.BooleanFilter(label="Verified only")

    # --- Ordering ---
    # ordering = django_filters.OrderingFilter(
    #     fields=(
    #         ("name",         "name"),
    #         ("rating",       "rating"),
    #         ("review_count", "review_count"),
    #         ("created_at",   "created_at"),
    #     ),
    #     label="Order by",
    # )

    search = django_filters.CharFilter(
        method="filter_search",
        label="Search (name, description)",
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(description__icontains=value)
        )

    class Meta:
        model = Place
        fields = [
            "name", "type", "tags", "verified",
            "rating_min", "rating_max",
            "review_count_min", "review_count_max",
            "search", #"ordering",
        ]