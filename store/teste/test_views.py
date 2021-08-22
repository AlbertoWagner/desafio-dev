import os

from django.urls import reverse
from django.test import Client
from django.test import TestCase
from store.models import Stores

from transactions.models import Transaction
from django.conf import settings

HTTP_200 = 200
HTTP_302_CREATE = 302

# ------------------------------------------------------------------------
# To run
#  ./manage.py test store.teste
# ------------------------------------------------------------------------


class StoreTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_views_store_list(self):
        response = self.client.get(reverse('store:store-list'))
        self.assertEqual(response.status_code, HTTP_200)
