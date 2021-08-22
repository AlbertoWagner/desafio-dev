from django.test import TestCase
from model_mommy import mommy
from store.models import Stores


# ------------------------------------------------------------------------
# To run
#  ./manage.py test store.teste
# ------------------------------------------------------------------------

class StoreModelTestCase(TestCase):

    def setUp(self):
        self.store = mommy.make(Stores)

    def test_store(self):
        store = Stores.objects.filter(name=self.store.name)
        self.assertEquals(store.exists(), True)
        self.assertEquals(store.all().count(), 1)

    def test_store_name(self):
        mommy.make(Stores, name='Teste')
        store = Stores.objects.filter(name='Teste')
        self.assertEquals(store.exists(), True)

    def test_store_owner(self):
        mommy.make(Stores, store_owner='JOÃO')
        store = Stores.objects.filter(store_owner='JOÃO')
        self.assertEquals(store.exists(), True)
