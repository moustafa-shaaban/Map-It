---
layout: doc
outline: [2, 3]
---

This page lists the sturcture of seattle application, and the files used to build it.

[[toc]]


## Models

This application has three database models, Hospital, School, Library.

### Hospital

The main data file which I downloaded from the Seattle Open Data website for the Hospitals dataset contains 12 columns, `OBJECTID`, `FACILITY`, `ADDRESS`, `SE_ANNO_CAD_DATA`, `CITY`, `ACUTE_CARE`, `GIS_EDT_DT`, `URL`, `TELEPHONE`, `GlobalID`, `x`, `y`.

::: tip
You can find more information about this dataset [here](https://data-seattlecitygis.opendata.arcgis.com/datasets/d475a7df08e14acd9f97ab6d5c02c61e_0/explore).
:::

In this project we are only interested in 4 columns:

* `FACILITY`: This column represent the name of each hospital.
* `ADDRESS`: This column represent the address of each hospital.
* `x`: This column represent the latitude of each hospital.
* `y`: This column represent the longitude of each hospital.

I represented this columns by 4 fields in a Django database model called Hospital

* `facility`: A Character Field with max length of 250 characters, allow null values and a default name value of `test` so it can handle null values (if there are any) in this dataset.
* `address`: A Character Field with max length of 250 characters, allow null values and a default address value of `test` so it can handle null values (if there are any) in this dataset.
* `latitude`: A Float Field that allow null values so it can handle null values (if there are any) in this dataset.
* `longitude`: A Float Field that allow null values so it can handle null values (if there are any) in this dataset.

```python
class Hospital(models.Model):
    """ Model Class represents each Hospital in Seattle """
    facility = models.CharField(max_length=250, null=True, default='test')
    address = models.CharField(max_length=250, null=True, default='test')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitals"

    def __str__(self):
        """Return string representation of the model"""
        return f"{self.facility} - {self.address}"
```

### School
The main data file which I downloaded from the Seattle Open Data website for the Private Schools dataset contains 12 columns, `OBJECTID`, `NAME`, `SCHOOL_STREET_ADDRESS`, `SCHOOL_CITY`, `CITY`, `SCHOOL_STATE`, `SCHOOL_ZIP`, `SCHOOL_COUNTY`, `PUBLIC_SCHOOL_DISTRICT`, `FOR_PROFIT_OR_NON_PROFIT`, `SE_ANNO_CAD_DATA`, `x`, `y`.

::: tip
You can find more information about this dataset [here](https://data-seattlecitygis.opendata.arcgis.com/datasets/b6de4b1fca644618a60c2a72cbdbbfe5_0/explore).
:::

In this project we are only interested in 4 columns:

* `NAME`: This column represent the name of each school.
* `SCHOOL_STREET_ADDRESS`: This column represent the address of each school.
* `x`: This column represent the latitude of each school.
* `y`: This column represent the longitude of each school.

I represented this columns by 4 fields in a Django database model called School

* `name`: A Character Field with max length of 250 characters, allow null values and a default name value of `test` so it can handle null values (if there are any) in this dataset.
* `address`: A Character Field with max length of 250 characters, allow null values and a default address value of `test` so it can handle null values (if there are any) in this dataset.
* `latitude`: A Float Field that allow null values so it can handle null values (if there are any) in this dataset.
* `longitude`: A Float Field that allow null values so it can handle null values (if there are any) in this dataset.

```python
class School(models.Model):
    """ Model class represents Private Schools in Seattle """
    name = models.CharField(max_length=250, null=True, default='test')
    address = models.CharField(max_length=250, null=True, default='test')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "Schools"

    def __str__(self):
        """Return string representation of the model"""
        return f"{self.name} - {self.address}"
```

### Library
The main data file which I downloaded from the Seattle Open Data website for the Libraries dataset contains 9 columns, `OBJECTID`, `NAME`, `ADDRESS`, `SPECIAL`, `SHELTER`, `LABEL`, `WEBSITE`, `x`, `y`.

::: tip
You can find more information about this dataset [here](https://data-seattlecitygis.opendata.arcgis.com/datasets/1f1acee596164245968375e9a456e07c_0/explore).
:::

In this project we are only interested in 4 columns:

* `NAME`: This column represent the name of each library.
* `ADDRESS`: This column represent the address of each library.
* `x`: This column represent the latitude of each library.
* `y`: This column represent the longitude of each library.

I represented this columns by 4 fields in a Django database model called Library

* `name`: A Character Field with max length of 250 characters, allow null values and a default name value of `test` so it can handle null values (if there are any) in this dataset.
* `address`: A Character Field with max length of 250 characters, allow null values and a default address value of `test` so it can handle null values (if there are any) in this dataset.
* `latitude`: A Float Field that allow null values so it can handle null values (if there are any) in this dataset.
* `longitude`: A Float Field that allow null values so it can handle null values (if there are any) in this dataset.


```python
class Library(models.Model):
    """Model class represents a Library in Seattle"""
    name = models.CharField(max_length=250, null=True, default='test')
    address = models.CharField(max_length=250, null=True, default='test')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        verbose_name = "Library"
        verbose_name_plural = "Libraries"

    def __str__(self):
        """Return string representation of the model"""
        return f"{self.name} - {self.address}"
```

## Resources

This file has three resources that represents database models, these resources will be used by `django-import-export` package to handle data import/export from both the Django admin site and django views and templates.

each resource extends the `ModelResource` of `django-import-export` package.

::: tip
You can learn more about ModelResource [here](https://django-import-export.readthedocs.io/en/latest/api_resources.html#modelresource).
:::

```python
from import_export import resources
from .models import Hospital, School, Library


class HospitalResource(resources.ModelResource):
    class Meta:
        model = Hospital


class SchoolResource(resources.ModelResource):
    class Meta:
        model = School


class LibraryResource(resources.ModelResource):
    class Meta:
        model = Library
```



## Admin

This file is used to register the database models used for `CRUD` (Create, Read, Update and Delete) actions for each model, and, three classed that extends `ImportExportModelAdmin` from `django-import-export` to add the functionality of importing/exporting data from the Django admin site

```python
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Hospital, School, Library
from .resources import HospitalResource, SchoolResource, LibraryResource


class HospitalAdmin(ImportExportModelAdmin):
    resource_class = HospitalResource


class SchoolAdmin(ImportExportModelAdmin):
    resource_class = SchoolResource


class LibraryAdmin(ImportExportModelAdmin):
    resource_class = LibraryResource


admin.site.register(Hospital, HospitalAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Library, LibraryAdmin)
```

## Filters

This file adds filtering functionality for the application that allows users to filter the data by name or address.
It uses `django-filter` package for filtering data easily. and has base class and three other classes one for each database model.

```python
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
    def filter_q(self, queryset, name, value):
        return queryset.filter(
            Q(facility__icontains=value) | Q(address__icontains=value)
        )

    class Meta:
        model = Hospital
        fields = ['q']
```

notice the `HospitalFilter` it filters the data by `facility` instead of `name` like the other two classes.

## URLS

Currently this application has 8 urls, the first url is for displaying the homepage, the secound is for the map view, and the rest of the urls is for handing data import/export for each model

```python
from django.urls import path

from . import views

app_name = 'seattle'


urlpatterns = [
    path('', views.HomePage.as_view(), name='seattle-homepage'),
    path('map/', views.map_view, name='seattle-map'),

    # Importing Data
    path('import-hospitals/', views.import_hospitals_data, name='import-hospitals'),
    path('import-schools/', views.import_schools_data, name='import-schools'),
    path('import-libraries/', views.import_libraries_data, name='import-libraries'),

    # Exporting Data
    path('export-hospitals/', views.export_hospitals_data, name='export-hospitals'),
    path('export-schools/', views.export_schools_data, name='export-schools'),
    path('export-libraries/', views.export_libraries_data, name='export-libraries'),

]
```

## Views

This application has three database models, Hospital, School, Library.

## Templates

This application has three database models, Hospital, School, Library.