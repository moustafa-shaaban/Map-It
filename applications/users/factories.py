import factory
from django.conf import settings
from factory.django import DjangoModelFactory
from factory import Faker, PostGenerationMethodCall
from django.db.models.signals import post_save

from .models import Profile

@factory.django.mute_signals(post_save) 
class UserFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username', 'email',) 

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    
    password = PostGenerationMethodCall('set_password', '1234') 
    is_active = True
    is_staff = False

    @factory.lazy_attribute_sequence
    def username(self, n):
        return f"{self.first_name}_{self.last_name}_{n}".lower()

    @factory.lazy_attribute_sequence
    def email(self, n):
        return f"{self.first_name}.{self.last_name}.{n}@example.com".lower()

    @factory.post_generation
    def set_superuser_status(self, create, extracted, **kwargs):
        if extracted:
            self.is_staff = True
            self.is_superuser = True
            self.save()

    @factory.post_generation
    def create_profile(self, create, extracted, **kwargs):
        if not create:
            return
        ProfileFactory(user=self) 

    class Params:
        is_superuser = factory.Trait(
            set_superuser_status=True,
        )

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    avatar = factory.django.ImageField(width=200, height=200, color=Faker('color'))
    bio = factory.Faker('paragraph', nb_sentences=3)
    date_of_birth = factory.Faker('date_of_birth', minimum_age=15, maximum_age=30)