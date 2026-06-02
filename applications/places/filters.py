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

    min_rating = django_filters.NumberFilter(
        field_name="avg_rating",
        lookup_expr="gte",
        label="Minimum rating",
    )
    max_rating = django_filters.NumberFilter(
        field_name="avg_rating",
        lookup_expr="lte",
        label="Maximum rating",
    )

    min_review_count = django_filters.NumberFilter(
        field_name="review_count",
        lookup_expr="gte",
        label="Minimum review count",
    )
    max_review_count = django_filters.NumberFilter(
        field_name="review_count",
        lookup_expr="lte",
        label="Maximum review count",
    )

    verified = django_filters.BooleanFilter(label="Verified only")

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
            "min_rating", "max_rating",
            "min_review_count", "max_review_count",
            "search",
        ]