from decimal import Decimal
import random
import factory
from factory.django import DjangoModelFactory
import numpy as np
from faker import Faker

from applications.seattle.utils import normalize_text
from .models import Type, Place, Tag

fake = Faker()


def realistic_rating():
    raw = np.random.normal(loc=4.0, scale=0.6)
    return round(max(1.0, min(5.0, raw)), 1)


def realistic_review_count():
    return max(1, int(np.random.lognormal(mean=4.5, sigma=1.2)))


def coordinates_on_land(country_code=None):
    if country_code:
        result = fake.local_latlng(country_code=country_code)
        if result is None:
            raise ValueError(f"No location data available for country: {country_code}")
        return result[0], result[1]

    lat, lon = fake.location_on_land(coords_only=True)
    return lat, lon


class TypeFactory(DjangoModelFactory):
    class Meta:
        model = Type
        django_get_or_create = ('name',)

    name = factory.Iterator([
        'Restaurant', 'Cafe', 'Park', 'Hotel',
        'Shopping Mall', 'Library', 'Cinema', 'Gym', 'Hospital', 'School',
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
        'Vegetarian options', 'Vegan options', 'Organic',
        'Budget-friendly', 'Luxury', 'Open 24 Hour'
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
    type = factory.SubFactory(TypeFactory)
    rating = factory.LazyFunction(realistic_rating)
    review_count = factory.LazyFunction(realistic_review_count)
    phone = fake.phone_number()
    verified = random.random() > 0.25
    website = factory.LazyAttribute(lambda o: '%s.com' % o.name)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        country_code = kwargs.pop('country_code', None)
        lat, lon = coordinates_on_land(country_code)
        kwargs['latitude'] = lat
        kwargs['longitude'] = lon
        return super()._create(model_class, *args, **kwargs)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            tags_to_add = TagFactory.create_batch(fake.random_int(min=2, max=4))
            for tag in tags_to_add:
                self.tags.add(tag)