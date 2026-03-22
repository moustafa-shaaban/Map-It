import django_filters
from django.db.models import Q
from .models import Hospital, School, Library

class LocationFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filter_q', label='Search')

    def filter_q(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(address__icontains=value)
        )

    class Meta:
        # Base filter - will be subclassed per model
        fields = ['q']


class SchoolFilter(LocationFilter):
    class Meta:
        model = School
        fields = ['q']

class LibraryFilter(LocationFilter):
    class Meta:
        model = Library
        fields = ['q']

class HospitalFilter(LocationFilter):
    # Hospital uses 'facility' instead of 'name'
    def filter_q(self, queryset, name, value):
        return queryset.filter(
            Q(facility__icontains=value) | Q(address__icontains=value)
        )

    class Meta:
        model = Hospital
        fields = ['q']