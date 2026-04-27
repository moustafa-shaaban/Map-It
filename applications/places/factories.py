from decimal import Decimal
import random
import factory
from factory.django import DjangoModelFactory
import numpy as np
from faker import Faker
from django.core.management.base import BaseCommand
from django.db import transaction
import pycountry

from applications.seattle.utils import normalize_text

from .models import Category, Place, Tag

fake = Faker()


def realistic_rating():
    raw = np.random.normal(loc=4.0, scale=0.6)
    return round(max(1.0, min(5.0, raw)), 1)


def realistic_review_count():
    return max(1, int(np.random.lognormal(mean=4.5, sigma=1.2)))


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.Iterator([
        'Restaurant', 'Cafe', 'Park', 'Museum', 'Hotel', 
        'Shopping Mall', 'Beach', 'Historical Site', 'Library', 
        'Cinema', 'Gym', 'Hospital', 'School',
    ])

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if 'name' in kwargs:
            kwargs['name'] = normalize_text(kwargs['name'])
        return super()._create(model_class, *args, **kwargs)


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = factory.Iterator([
        'Family-friendly', 'Pet-friendly', 'Wheelchair accessible', 
        'Free Wi-Fi', 'Parking available', 'Outdoor seating', 
        'Vegetarian options', 'Vegan options', 'Organic', 'Local cuisine',
        'Historical', 'Artistic', 'Budget-friendly', 'Luxury'
    ])

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if 'name' in kwargs:
            kwargs['name'] = normalize_text(kwargs['name'])
        return super()._create(model_class, *args, **kwargs)

class PlaceFactory(DjangoModelFactory):

    class Meta:
        model = Place

    name = factory.LazyAttribute(lambda _: fake.company() if fake.boolean() else fake.street_name())
    description = factory.LazyAttribute(lambda _: fake.paragraph(nb_sentences=3))
    category = factory.SubFactory(CategoryFactory)
    rating = factory.LazyFunction(realistic_rating)
    review_count = factory.LazyFunction(realistic_review_count)
    phone = fake.phone_number()
    verified = random.random() > 0.25
    website = factory.LazyAttribute(lambda o: '%s.com' % o.name)

    latitude = factory.LazyFunction(
        lambda: Decimal(str(fake.location_on_land(coords_only=True)[0]))
    )

    longitude = factory.LazyFunction(
        lambda: Decimal(str(fake.location_on_land(coords_only=True)[1]))
    )
        
    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            # If tags are provided, use them
            for tag in extracted:
                self.tags.add(tag)
        else:
            # Otherwise add 2-4 random tags
            tags_to_add = TagFactory.create_batch(fake.random_int(min=2, max=4))
            for tag in tags_to_add:
                self.tags.add(tag)