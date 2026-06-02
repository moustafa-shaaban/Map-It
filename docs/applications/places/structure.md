---
layout: doc
outline: [2, 3]
---

This page lists the sturcture of seattle application, and the files used to build it.

[[toc]]


## Utils

We start by a very useful utility function that will be used in many actions in the project, it's main functionality is to remove some special characters, trim/strip white spaces from text and save strings data in lower-case.

This is useful becuase we need to make sure that the data (type and tag names) are unique.

```python
from django.utils.encoding import force_str
from django.utils.text import slugify

def normalize_text(text, allow_unicode=False):
    """
    Enhanced normalization for uniqueness and security.
    """
    text = force_str(text or "")
    
    # 1. Handle Unicode: If allow_unicode is False, it converts 'café' to 'cafe'
    # Django's slugify handles the NFKD normalization and stripping of non-ascii 
    # more robustly than a manual re.sub.
    text = slugify(text, allow_unicode=allow_unicode)
    
    # 2. Manual refinements (if you specifically need / and spaces preserved)
    # Note: slugify replaces spaces with dashes. If you want spaces, 
    # we swap them back.
    text = text.replace('-', ' ')
    
    # 3. Security: Prevent "Hidden" characters
    # Some unicode characters look like spaces but aren't. 
    # .split() handles all whitespace types (tabs, newlines, etc.)
    return " ".join(text.split()).lower().strip()
```

## Models

This application has three database models, Hospital, place, Library. each model have a database unique constraint on the `facility/name` field to make sure the data is unqiue, and a save method that uses `normalize_text` util on the `facility/name` + `address` fields to noramilze its content.

### Type

This model only has one field `name` that represents the type of a place (hospital, gym, ...)

```python
class Type(models.Model):
    """Model definition for Type."""

    name = models.CharField(max_length=50)

    class Meta:
        """Meta definition for Type."""

        verbose_name = 'Type'
        verbose_name_plural = 'Type'

    def __str__(self):
        """Unicode representation of Type."""
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = normalize_text(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Type."""
        return reverse('type-detail', kwargs={'pk': self.pk})
```

### Tag

This model only has one field `name` that represents the tag of a place (open-24h, pet-friendly, ...)

```python
class Tag(models.Model):
    """Model definition for Tag."""

    name = models.CharField(max_length=50)

    class Meta:
        """Meta definition for Tag."""

        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        """Unicode representation of Tag."""
        return f"{self.name}"

    def save(self, *args, **kwargs):
        """Save method for Tag."""
        if self.name:
            self.name = normalize_text(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Tag."""
        return reverse('tag-detail', kwargs={'pk': self.pk})
```

### Place

This model only has 11 fields.

* `name`: This column represent the name of each place.
* `description`: This column represent the address of each place.
* `type`: This column represent a one-to-many relationship between the Type and Place models, `on_delete=models.CASCADE` means that if a Type instance in the database is deleted, all the places associated with it will be deleted as well.
* `tags`: This column represent a many-to-many relationship between the Tag and Place models.
* `phone`: This column represent the phone of each place.
* `website`: This column represent the website url of each place.
* `verified`: This column represents if the place is verified or not, this will be managed by the website admins.
* `latitude`: This column represent the longitude of each place.
* `longitude`: This column represent the longitude of each place.
* `created_at`: A timestamp field that displays when the place is created.
* `updated_at`: A timestamp field that displays when the place is updated.

```python
class Place(models.Model):
    """Model definition for Place."""

    name = models.CharField(max_length=250)
    description = models.TextField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    phone = models.CharField(max_length=30)
    website = models.URLField()
    verified = models.BooleanField(default=False, db_index=True)
    latitude  = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Place."""

        verbose_name = 'Place'
        verbose_name_plural = 'Places'
        indexes = [
            models.Index(fields=["type"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        """Unicode representation of Place."""
        return f"{self.name} - ({self.type})"

    def get_absolute_url(self):
        """Return absolute url for Place."""
        return reverse('place-detail', kwargs={'pk': self.pk})
```

### Review

This model only has 5 fields.

* `place`: This column represent a one-to-many relationship between the Review and Place models, `on_delete=models.CASCADE` means that if a Place instance in the database is deleted, all the reviews associated with it will be deleted as well.
* `user`: This column represent a one-to-many relationship between the Review and User models, `on_delete=models.CASCADE` means that if a User instance in the database is deleted, all the reviews associated with it will be deleted as well..
* `rating`: This column represent the rating a user selected for a place.
* `comment`: This column represent the commnet a user added to describe a place.
* `created_at`: A timestamp field that displays when the place is created.

```python
class Review(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Review."""

        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        """Unicode representation of Review."""
        return f"{self.user} - {self.place}"

    def get_absolute_url(self):
        """Return absolute url for Review."""
        return reverse('review-detail', kwargs={'pk': self.pk})
```

* Full `applications/places/models.py` code

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.text import slugify
from django.conf import settings

def normalize_text(text, allow_unicode=False):
    """
    Enhanced normalization for uniqueness and security.
    """
    text = force_str(text or "")
    
    # 1. Handle Unicode: If allow_unicode is False, it converts 'café' to 'cafe'
    # Django's slugify handles the NFKD normalization and stripping of non-ascii 
    # more robustly than a manual re.sub.
    text = slugify(text, allow_unicode=allow_unicode)
    
    # 2. Manual refinements (if you specifically need / and spaces preserved)
    # Note: slugify replaces spaces with dashes. If you want spaces, 
    # we swap them back.
    text = text.replace('-', ' ')
    
    # 3. Security: Prevent "Hidden" characters
    # Some unicode characters look like spaces but aren't. 
    # .split() handles all whitespace types (tabs, newlines, etc.)
    return " ".join(text.split()).lower().strip()


class Type(models.Model):
    """Model definition for Type."""

    name = models.CharField(max_length=50)

    class Meta:
        """Meta definition for Type."""

        verbose_name = 'Type'
        verbose_name_plural = 'Type'

    def __str__(self):
        """Unicode representation of Type."""
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = normalize_text(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Type."""
        return reverse('type-detail', kwargs={'pk': self.pk})


class Tag(models.Model):
    """Model definition for Tag."""

    name = models.CharField(max_length=50)

    class Meta:
        """Meta definition for Tag."""

        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        """Unicode representation of Tag."""
        return f"{self.name}"

    def save(self, *args, **kwargs):
        """Save method for Tag."""
        if self.name:
            self.name = normalize_text(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Tag."""
        return reverse('tag-detail', kwargs={'pk': self.pk})
    

class Place(models.Model):
    """Model definition for Place."""

    name = models.CharField(max_length=250)
    description = models.TextField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    phone = models.CharField(max_length=30)
    website = models.URLField()
    verified = models.BooleanField(default=False, db_index=True)
    latitude  = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Place."""

        verbose_name = 'Place'
        verbose_name_plural = 'Places'
        indexes = [
            models.Index(fields=["type"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        """Unicode representation of Place."""
        return f"{self.name} - ({self.type})"

    def get_absolute_url(self):
        """Return absolute url for Place."""
        return reverse('place-detail', kwargs={'pk': self.pk})


class Review(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Review."""

        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        """Unicode representation of Review."""
        return f"{self.user} - {self.place}"

    def get_absolute_url(self):
        """Return absolute url for Review."""
        return reverse('review-detail', kwargs={'pk': self.pk})
```

## Admin

This file is used to register the database models used for `CRUD` (Create, Read, Update and Delete) actions for each model, and, three classed that extends `admin.ModelAdmin` to improve data interactions in the admin site. (searching, listing and filtering data)

```python
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


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ("place", "user", "rating", "created_at")
    search_fields = ["place", "user"]
    list_filter = ["rating"]

admin.site.register(Type, TypeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Review, ReviewAdmin)
```

## Filters

This file adds filtering functionality for the application that allows users to filter the data by `name`, `tags`, `type`, min and max ratings using `min_rating` and `max_rating`, min and max review counts using `min_review_count` and `max_review_count`, `verified`, and searching for a place using its name or description with a custome filter function called `filter_search`.

```python
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
```

