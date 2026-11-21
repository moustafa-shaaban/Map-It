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