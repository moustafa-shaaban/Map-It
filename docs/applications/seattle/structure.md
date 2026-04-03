---
layout: doc
outline: [2, 3]
---

This page lists the sturcture of seattle application, and the files used to build it.

[[toc]]


## Utils

I start by a very useful util function that will be used to many actions in the project, it's main functionality is to remove some special characters, trim/strip white spaces from text and save strings data in lower-case.

This is useful becuase we need to make sure that the data (facility name for hospitals, and name for schools and libraries) are unique.

```python
from django.utils.encoding import force_str
import unicodedata
import re

def normalize_text(text):
    """Full normalization for uniqueness. Writen with help from Grok AI"""
    text = force_str(text or "") # Source: https://docs.djangoproject.com/en/6.0/ref/utils/#django.utils.encoding.force_str
    text = unicodedata.normalize("NFKD", text).lower() # Lower-case text then emove accents ("café" to "cafe") Source: https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize
    text = re.sub(r"[^a-z0-9\s\-\/]", "", text) # Accept only A to Z + 0 to 9 and dash ( - ) + forward slash ( / )
    # Collapse multiple whitespace into single space and strip
    return " ".join(text.split())
```

## Models

This application has three database models, Hospital, School, Library. each model have a database unique constraint on the `facility/name` field to make sure the data is unqiue, and a save method that uses `normalize_text` util on the `facility/name` + `address` fields to noramilze its content.

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

I represented these columns by 4 fields in a Django model called Hospital

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

I represented these columns by 4 fields in a Django database model called School

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

I exclude the `id` from each model. and each model have a `before_import_row` function that handles normalizing text, before passing the data to preview page so the user can see the data before it is sent to the database.

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

This file is used to register the database models used for `CRUD` (Create, Read, Update and Delete) actions for each model, and, three classed that extends `ImportExportModelAdmin` from `django-import-export` to add the functionality of importing/exporting data from the Django admin site.

I also added the functionality of listing each admin model by all the fields, and searching on each admin model by `facility/name` + `address` fields.

```python
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
```

## Filters

This file adds filtering functionality for the application that allows users to filter the data by `name` or `address`.

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

## Forms

Here, there are two forms `UploadFileForm` and `ExportForm`.

### UploadFileForm

This form is used for validating the files that users upload. It has three backend levels of validation:

1. Validating the file extension using Django's bulit-in `FileExtensionValidator`. This makes sure that only three file extensions are allowed (`csv`, `xlsx`, and `json`).
2. Validating the uploaded file size. This make sure that the user cannot upload a file that is larger than 5MB.
3. Validating the uoloaded file extension based on it's mime using `python-magic` package. This very important because without it, a malicious user can upload any type of files by just changing its extension, for example, a `file.exe` could be changed to `file.csv` and it will bypass the first validation level (using `FileExtensionValidator`).

There is another validation rule added to the fontend by passing `'accept': '.csv,.xlsx,.json'` attribute as a widget for the form FileField, but we should not rely on it because it can be easily bypassd in the frontend.


```python
from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

import magic

extension_validators = [
    'csv',
    'xlsx',
    'json'
]

def validate_file_size(file):
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError(f'File exceeded the maximum size. Max size is 5MB.')
    

def validate_file_type(file):
    file_content = file.read(4096)
    file.seek(0)
    mime = magic.from_buffer(file_content, mime=True)
    
    allowed_mimes = [
        'text/csv', 
        'application/json',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/plain',
        'application/zip',
    ]
    if mime not in allowed_mimes:
        raise ValidationError('The file content does not match the allowed types, (.csv, .xlsx, .json)')
    

class UploadFileForm(forms.Form):
    import_file = forms.FileField(
        label='Select file',
        validators=[FileExtensionValidator(allowed_extensions=extension_validators), validate_file_size, validate_file_type],
        widget=forms.FileInput(
            attrs={
                'name': 'import_file',
                'class': 'form-control', 
                'accept': '.csv,.xlsx,.json',
            }
        )
    )
```

### ExportForm

A simple form that asks the user to choose the type of the file they want to export, currently it supports only three types of files (csv, xlsx, and json).

## Mixins

Here, there are two reusable mixins used for importing and exporting data using `django-import-export` package. (both `Deepseek` and `Grok` ai helped me a lot im writing these mixins).

### BaseDataImport

This mixin extends Django's built-in `View` class and can be subclassed by four attributes `model`, `template_name`, `resource_class` and `success_url`.

This class have the following functions:

1. `add_success_message` is used to generate success message after importing data. I copied a some of it's actions from the `django-import-export` package. exactly from [here](https://github.com/django-import-export/django-import-export/blob/main/import_export/admin.py). The name of the function is `add_success_message` and is currenntly on line number `259`.

```python

def add_success_message(self, result, request):
    if not result.has_errors() and result.total_rows == 0:
        messages.warning(request, _("Import completed, but no records were changed."))
        return
    if not self.model:
        # Fallback if model isn't defined: use a generic name
        plural_name = "records"
    else:
        plural_name = self.model._meta.verbose_name_plural
    success_message = _(
        "Import finished: {} new, {} updated, {} deleted and {} skipped {}."
    ).format(
        result.totals.get(RowResult.IMPORT_TYPE_NEW, 0),
        result.totals.get(RowResult.IMPORT_TYPE_UPDATE, 0),
        result.totals.get(RowResult.IMPORT_TYPE_DELETE, 0),
        result.totals.get(RowResult.IMPORT_TYPE_SKIP, 0),
        plural_name,
    )
    messages.success(request, success_message)

```

This function counts the number 0f new, updated, deleted or skipped row after confirming data upload.

2. `get_success_url` this function redirects the user to a given url after data import is successful.

```python

def get_success_url(self):
    return self.success_url

```

3. `get` this function passes the `UploadFileForm` as a context to the template on `GET` requests.

```python

def get(self, request):
    form = UploadFileForm()
    return render(request, self.template_name, {'form': form})

```

4. `post`now this function handles the `POST` request that is send to the view, and it has some steps that handle previewing data, canceling import, parsing the uploaded file and finally confirming data import.

```python

def post(self, request):
    # 1. define the django-import-export resource to use
    resource = self.resource_class()

    """
    2. If the user canceled data importing, check if the session have cached data, if the session have data then delete it, and inform the user that the data from the file they uploaded is not mported to the database. Finally redirect the user to the data import page.
    """
    if 'cancel_import' in request.POST:
        if 'import_data_cache' in request.session:
            del request.session['import_data_cache']
        messages.info(request, "Import cancelled and temporary data cleared.")
        return redirect(request.path)

    
    # 3. If the user confirmed data import, call the `handle_confirmation function.
    if 'confirm_import' in request.POST:
        return self.handle_confirmation(request, resource)
    
    
    # 4. Instantiate the UploadFileForm with with the file posted by the user
    form = UploadFileForm(request.POST, request.FILES)

    """
    # 5. If the form is valid do the following: 
        - Get the cleaned file from the form then try to create a tablib dataset by passing the file to the `parse_file` function
        - Add the data to the user's session so the file is not lost when moving from previewing the data to importing it, this way will make sure that the user does not have to upload the file twice.
        - create a result using django-import-export resource import_data function and make sure to add (dry_run=True) to tell django-import-export that we are not ready to import the data yet.
        - Pass the sesult to as a context for the template so the user can preview the data before confirming data import.
        - If the code failed to add the data to user's session and pass it for previewing, raise and Exception with a message that has the error.
        - If the form is not valid render the template with form validation errors.

    """
    if form.is_valid():
        import_file = form.cleaned_data['import_file']
        
        try:
            dataset = self.parse_file(import_file)
            
            request.session['import_data_cache'] = dataset.dict
            
            result = resource.import_data(dataset, dry_run=True)
            return render(request, self.template_name, {
                'result': result,
                'form': form
            })
        except Exception as e:
            messages.error(request, f"Parsing error: {str(e)}")
            return render(request, self.template_name, {'form': form})
        
    else:
        return render(request, self.template_name, {'form': form})

    
    """
    6. the parse_file function accepts the uploaded file and checks its extension and based on the result it uses the correct format of the file
    """
    def parse_file(self, import_file):
        dataset = Dataset()
        extension = import_file.name.split('.')[-1].lower()
        content = import_file.read()
        
        if extension == 'csv':
            dataset.load(content.decode('utf-8'), format='csv')
        elif extension == 'xlsx':
            dataset.load(content, format='xlsx')
        elif extension == 'json':
            dataset.load(content.decode('utf-8'), format='json')
        else:
            raise ValueError("Unsupported extension.")
        return dataset

    """
    7. the handle_confirmation function does the following
        - Read the data from user's session
        - see the data that the user selected for import
        - If there are no data in the seeion or the user did not select any rows return an error and redirect the user to data import page.
        - If the user selected data rows filter the data in session based on what data the user selected and create a tablib dataset from the filtered data
        - import the data using django-import-export resource import_data function and this time add (dry_run=False) to import the data into the database.
        - delete the session data, to make it ready for another data preview/import flow.
        - add a success message and then redirect the user to the import page.
    """
    def handle_confirmation(self, request, resource):
        import_data = request.session.get('import_data_cache')
        selected_indices = request.POST.getlist('selected_rows')

        if not import_data or not selected_indices:
            messages.error(request, "Session expired or no rows selected.")
            return redirect(request.path)

        filtered_data = [import_data[int(i)] for i in selected_indices]
        dataset = Dataset()
        dataset.dict = filtered_data
        
        result = resource.import_data(dataset, dry_run=False)
        del request.session['import_data_cache']
        self.add_success_message(result, request)
        return redirect(self.success_url)

```

### BaseDataExport

## Views

TODO

## Templates

TODO