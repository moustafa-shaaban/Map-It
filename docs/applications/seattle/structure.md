---
layout: doc
outline: [2, 3]
---

This page lists the sturcture of seattle application, and the files used to build it.

[[toc]]


## Utils

We start by a very useful util function that will be used to many actions in the project, it's main functionality is to remove some special characters, trim/strip white spaces from text and save strings data in lower-case.

This is useful becuase we need to make sure that the data (facility name for hospitals, and name for schools and libraries) are unique.

```python
from django.utils.encoding import force_str
import unicodedata
import re

def normalize_text(text):
    text = force_str(text or "")
    text = unicodedata.normalize("NFKD", text).lower()
    text = re.sub(r"[^a-z0-9\s\-\/]", "", text)
    return " ".join(text.split())
```

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
        constraints = [
            models.UniqueConstraint(
                Lower(Trim('facility')),
                name='unique_clean_hospital_facility'
            )
        ]

    def __str__(self):
        """Return string representation of the model"""
        return f"{self.facility} - {self.address}"
        
    def save(self, *args, **kwargs):
        if self.facility:
            self.facility = normalize_text(self.facility)
        if self.address:
            self.address = normalize_text(self.address)
        super().save(*args, **kwargs)
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
        constraints = [
            models.UniqueConstraint(
                Lower(Trim('name')),
                name='unique_clean_school_name'
            )
        ]

    def __str__(self):
        """Return string representation of the model"""
        return f"{self.name} - {self.address}"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = normalize_text(self.name)
        if self.address:
            self.address = normalize_text(self.address)
        super().save(*args, **kwargs)
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
        constraints = [
            models.UniqueConstraint(
                Lower(Trim('name')),
                name='unique_clean_library_name'
            )
        ]

    def __str__(self):
        """Return string representation of the model"""
        return f"{self.name} - {self.address}"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = normalize_text(self.name)
        if self.address:
            self.address = normalize_text(self.address)
        super().save(*args, **kwargs)
```


* Full `models.py` code

```python
from django.db import models
from django.db.models.functions import Lower, Trim

from .utils import normalize_text


class Hospital(models.Model):
    """ Model Class represents each Hospital in Seattle """
    facility = models.CharField(max_length=250, null=True, default='test')
    address = models.CharField(max_length=250, null=True, default='test')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitals"
        constraints = [
            models.UniqueConstraint(
                Lower(Trim('facility')),
                name='unique_clean_hospital_facility'
            )
        ]

    def __str__(self):
        """Return string representation of the model"""
        return f"{self.facility} - {self.address}"
        
    def save(self, *args, **kwargs):
        if self.facility:
            self.facility = normalize_text(self.facility)
        if self.address:
            self.address = normalize_text(self.address)
        super().save(*args, **kwargs)


class School(models.Model):
    """ Model class represents Private Schools in Seattle """
    name = models.CharField(max_length=250, null=True, default='test')
    address = models.CharField(max_length=250, null=True, default='test')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "Schools"
        constraints = [
            models.UniqueConstraint(
                Lower(Trim('name')),
                name='unique_clean_school_name'
            )
        ]

    def __str__(self):
        """Return string representation of the model"""
        return f"{self.name} - {self.address}"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = normalize_text(self.name)
        if self.address:
            self.address = normalize_text(self.address)
        super().save(*args, **kwargs)


class Library(models.Model):
    """Model class represents a Library in Seattle"""
    name = models.CharField(max_length=250, null=True, default='test')
    address = models.CharField(max_length=250, null=True, default='test')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        verbose_name = "Library"
        verbose_name_plural = "Libraries"
        constraints = [
            models.UniqueConstraint(
                Lower(Trim('name')),
                name='unique_clean_library_name'
            )
        ]

    def __str__(self):
        """Return string representation of the model"""
        return f"{self.name} - {self.address}"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = normalize_text(self.name)
        if self.address:
            self.address = normalize_text(self.address)
        super().save(*args, **kwargs)

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
from .utils import normalize_text

class HospitalResource(resources.ModelResource):
    class Meta:
        model = Hospital
        exclude = ('id',)
        import_id_fields = ('facility',)
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        if row.get('facility'):
            row['facility'] = normalize_text(row['facility'])
        if row.get('address'):
            row['address'] = normalize_text(row['address'])
    


class SchoolResource(resources.ModelResource):
    class Meta:
        model = School
        import_id_fields = ('name',)
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        if row.get('name'):
            row['name'] = normalize_text(row['name'])
        if row.get('address'):
            row['address'] = normalize_text(row['address'])


class LibraryResource(resources.ModelResource):
    class Meta:
        model = Library
        import_id_field = ('name',)
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        if row.get('name'):
            row['name'] = normalize_text(row['name'])
        if row.get('address'):
            row['address'] = normalize_text(row['address'])
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
    path('import-hospitals/', views.ImportHospitalsView.as_view(), name='import-hospitals'),
    path('import-schools/', views.ImportSchoolsView.as_view(), name='import-schools'),
    path('import-libraries/', views.ImportLibrariesView.as_view(), name='import-libraries'),

    # Exporting Data
    path('export-hospitals/', views.HospitalsExportView.as_view(), name='export-hospitals'),
    path('export-schools/', views.SchoolsExportView.as_view(), name='export-schools'),
    path('export-libraries/', views.LibrariesExportView.as_view(), name='export-libraries'),

]
```

## Views

TODO

## Templates

TODO