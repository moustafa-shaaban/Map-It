# models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from applications.seattle.utils import normalize_text


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=50)

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Category."""
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = normalize_text(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Category."""
        return reverse('category-detail', kwargs={'pk': self.pk})


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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    rating = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    phone = models.CharField(max_length=30)
    website = models.URLField()
    review_count = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(default=False, db_index=True)
    latitude  = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Place."""

        verbose_name = 'Place'
        verbose_name_plural = 'Places'
        ordering = ["-rating", "-review_count"]
        indexes = [
            
            models.Index(fields=["category"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        """Unicode representation of Place."""
        return f"{self.name} - ({self.category}) - ({self.rating})"

    def save(self, *args, **kwargs):
        """Save method for Tag."""
        if self.name:
            self.name = normalize_text(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Place."""
        return reverse('place-detail', kwargs={'pk': self.pk})





# class Place(models.Model):

#     class PlaceType(models.TextChoices):
#         HOSPITAL   = "Hospital", "Hospital"
#         PARK       = "Park", "Park"
#         SCHOOL     = "School", "School"
#         RESTAURANT = "Restaurant", "Restaurant"
#         HOTEL      = "Hotel", "Hotel"
#         MUSEUM     = "Museum", "Museum"

#     name = models.CharField(max_length=200, db_index=True)
#     address = models.TextField()
#     city = models.CharField(max_length=100, db_index=True)
#     country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="places")
#     type = models.CharField(max_length=20, choices=PlaceType.choices, db_index=True)

#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)

#     rating = models.DecimalField(
#         max_digits=2, decimal_places=1,
#         validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
#     )
#     review_count = models.PositiveIntegerField(default=0)

#     phone = models.CharField(max_length=30, blank=True)
#     verified = models.BooleanField(default=False, db_index=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["-rating", "-review_count"]
#         indexes = [
#             models.Index(fields=["type", "country"]),
#             models.Index(fields=["latitude", "longitude"]),
#         ]

#     def __str__(self):
#         return f"{self.name} ({self.type}) — {self.city}"

