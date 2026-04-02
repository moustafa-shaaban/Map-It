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
