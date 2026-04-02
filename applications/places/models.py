# models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# class Country(models.Model):
#     code = models.CharField(max_length=2, unique=True, db_index=True)
#     name = models.CharField(max_length=100, unique=True)

#     class Meta:
#         verbose_name_plural = "countries"
#         ordering = ["name"]

#     def __str__(self):
#         return f"{self.name} ({self.code})"


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


# class OpeningHours(models.Model):
#     class DayGroup(models.TextChoices):
#         ALL_WEEK = "all_week", "All Week"
#         WEEKDAYS = "weekdays", "Weekdays Only"
#         WEEKENDS = "weekends", "Weekends Only"
#         CUSTOM = "custom", "Custom"

#     place = models.OneToOneField(Place, on_delete=models.CASCADE, related_name="opening_hours")
#     open_time = models.TimeField(null=True, blank=True)   # null = open 24h
#     close_time = models.TimeField(null=True, blank=True)   # null = open 24h
#     is_24_7 = models.BooleanField(default=False)
#     days = models.CharField(max_length=20, choices=DayGroup.choices, default=DayGroup.ALL_WEEK)
#     note = models.CharField(max_length=100, blank=True)

#     class Meta:
#         verbose_name_plural = "opening hours"

#     def __str__(self):
#         if self.is_24_7:
#             return f"{self.place.name}: 24/7"
#         return f"{self.place.name}: {self.open_time}–{self.close_time}"