import datetime
from django import forms
from django.core.exceptions import ValidationError

def validate_birth_date(value):
    today = datetime.date.today()
    if value >= today:
        raise ValidationError("Date of birth cannot be today or in the future.")
    # Optional: Check if the user is at least 15 years old
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 15:
        raise ValidationError("You must be at least 15 years old.")
