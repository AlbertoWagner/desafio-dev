import os

from django.urls import reverse
from django.test import Client
from django.test import TestCase
from store.models import Stores

from transactions.models import Transaction
from django.conf import settings

BASE_DIR = settings.BASE_DIR
DIR_CNAB = 'transactions/teste/arquivos/CNAB.txt'
DIR_FORMATO_ERRO = 'transactions/teste/arquivos/TESTE_FORMATO_ERRO.jpg'
DIR_TXT_ERRO = 'transactions/teste/arquivos/TXT_ERRO.txt'
HTTP_200 = 200
HTTP_302_CREATE = 302

# ------------------------------------------------------------------------
# To run
#  ./manage.py test transactions.teste
# ------------------------------------------------------------------------


class RegistrationTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def training__path(self, dir):
        return os.path.join(BASE_DIR, dir)

    def test_views_transactions_forms(self):
        self.myfile = open(self.training__path(DIR_CNAB), 'r')
        response = self.client.post(reverse('transactions:action'), {'file': self.myfile})
        self.assertEqual(response.status_code, HTTP_302_CREATE)
        # redirect sucesso
        self.assertEqual(response.url, '/store')
        self.assertEquals(Transaction.objects.filter(store__name='MERCADO DE TESTE').count(), 1)
        self.assertEquals(Transaction.objects.all().count(), 1)

    def test_views_transactions_forms_erros_suport(self):
        self.myfile_erro = open(self.training__path(DIR_FORMATO_ERRO), 'r')
        response = self.client.post(reverse('transactions:action'), {'file': self.myfile_erro})
        self.assertEqual(response.status_code, HTTP_200)
        MSG = response.content.decode('utf-8').split('\n')[54].split('strong')[1].replace('>', '').replace('</', '')
        self.assertEqual(MSG, 'Arquivo não suportado.')

    def test_views_transactions_forms_erros_format(self):
        self.myfile_erro = open(self.training__path(DIR_TXT_ERRO), 'r')
        response = self.client.post(reverse('transactions:action'), {'file': self.myfile_erro})
        self.assertEqual(response.status_code, HTTP_200)
        MSG = response.content.decode('utf-8').split('\n')[45].split('<')[0].split('>')[-1]
        self.assertEqual(MSG, 'Erro ao importa arquivo ')

    def test_views_transactions_list(self):
        self.test_views_transactions_forms()
        store = Stores.objects.filter(name='MERCADO DE TESTE')[0]
        response = self.client.get(reverse('transactions:transaction-list', args=[store.id]))
        self.assertEqual(response.status_code, HTTP_200)
