import factory.fuzzy as fuzzy
from factory.django import DjangoModelFactory


class ProductProxyFactory(DjangoModelFactory):
    class Meta:
        model = "gameshop.ProductProxy"

    title = fuzzy.FuzzyText()
    description = fuzzy.FuzzyText()
    price = fuzzy.FuzzyInteger(1, 1000)
    brand = fuzzy.FuzzyText()
