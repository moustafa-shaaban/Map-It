from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

from .models import Place, Type, Tag

class TypeForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = ['name',]

    

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name',]



class PlaceForm(forms.ModelForm):
    latitude = forms.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(Decimal('-90')), MaxValueValidator(Decimal('90'))],
        widget=forms.NumberInput(attrs={
            'id': 'id_latitude',
            'step': 'any',
            'placeholder': 'e.g. 30.044400',
            'class': 'coord-input',
        })
    )
    longitude = forms.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(Decimal('-180')), MaxValueValidator(Decimal('180'))],
        widget=forms.NumberInput(attrs={
            'id': 'id_longitude',
            'step': 'any',
            'placeholder': 'e.g. 31.235700',
            'class': 'coord-input',
        })
    )


    class Meta:
        model = Place
        fields = ['name', "description", "type", "tags", "phone", "website", "latitude", "longitude"]
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }