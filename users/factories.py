import factory.fuzzy

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.fuzzy.FuzzyText()
    last_name = factory.fuzzy.FuzzyText()
    username = factory.fuzzy.FuzzyText()
    password = factory.PostGenerationMethodCall('set_password', '12345678pP')
    # email = factory.fuzzy.FuzzyText()

    class Meta:
        model = User
