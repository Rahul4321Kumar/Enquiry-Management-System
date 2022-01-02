import factory

from factory.django import DjangoModelFactory

from users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    full_name = factory.Faker('name')
    # gender = factory.Faker('gender')
    