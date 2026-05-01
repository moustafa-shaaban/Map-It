from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from applications.seattle.utils import normalize_text


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
    rating = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(Decimal(1.0)), MaxValueValidator(Decimal(5.0))]
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
            
            models.Index(fields=["type"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        """Unicode representation of Place."""
        return f"{self.name} - ({self.type}) - ({self.rating})"

    def get_absolute_url(self):
        """Return absolute url for Place."""
        return reverse('place-detail', kwargs={'pk': self.pk})
