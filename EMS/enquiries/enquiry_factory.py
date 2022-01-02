import factory

from factory.django import DjangoModelFactory
from enquiries.models import Enquiry
from users.user_factory import UserFactory


class EnquiryFactory(DjangoModelFactory):
    class Meta:
        model = Enquiry
    
    # id = factory.Sequence(lambda n: ''.join(fake.random_elements(elements=(string.ascii_uppercase + string.digits), length=9, unique=True)).upper())
    user = factory.SubFactory(UserFactory)
    message = factory.Faker('text')
    