from django.test import TestCase
from model_mommy import mommy

from transactions.choices import ENTRADA, SUM, SAIDA, SUBTRACTION
from store.models import Stores
from transactions.models import TransactionType, Transaction


# ------------------------------------------------------------------------
# To run
#  ./manage.py test transactions.teste
# ------------------------------------------------------------------------

class TransactionTypeModelTestCase(TestCase):

    def setUp(self):
        self.transactions_type = mommy.make(TransactionType)

    def test_transactions_type(self):
        transactions_type = TransactionType.objects.filter(description=self.transactions_type.description)
        self.assertEquals(transactions_type.exists(), True)
        self.assertEquals(transactions_type.all().count(), 1)

    def test_transactions_type_description(self):
        mommy.make(TransactionType, description='Debito')
        transactions_type_debito = TransactionType.objects.filter(description='Debito')
        self.assertEquals(transactions_type_debito.exists(), True)


class TransactionModelTestCase(TestCase):

    def setUp(self):
        self.transactions_type = mommy.make(TransactionType)
        self.store = mommy.make(Stores)
        self.transactions = mommy.make(Transaction, transactions_type=self.transactions_type, store=self.store)

    def test_transactions(self):
        transactions_type = Transaction.objects.filter(cpf=self.transactions.cpf)
        self.assertEquals(transactions_type.exists(), True)
        self.assertEquals(transactions_type.all().count(), 1)

    def test_transactions_CPF(self):
        mommy.make(Transaction, cpf='09668512460')
        transactions = Transaction.objects.filter(cpf='09668512460')
        self.assertEquals(transactions.exists(), True)
        transactions = Transaction.objects.filter(cpf='096685**12460')
        self.assertEquals(transactions.exists(), False)

    def test_transactions_value(self):
        store_1 = mommy.make(Stores)
        transactions_type_1 = mommy.make(TransactionType, nature=ENTRADA, signal=SUM)
        transactions_1 = mommy.make(Transaction, store=store_1, value=1000, transactions_type=transactions_type_1)
        self.assertEquals(transactions_1.store.balance, 1000)
        self.assertEquals(transactions_1.value, 1000)
        self.assertEquals(transactions_1.get_display_value, 'R$ 1000.00')
        transactions_type_2 = mommy.make(TransactionType, nature=SAIDA, signal=SUBTRACTION)
        transactions_2 = mommy.make(Transaction, store=store_1, value=100, transactions_type=transactions_type_2)
        self.assertEquals(transactions_2.value, 100)
        self.assertEquals(transactions_2.get_display_value, 'R$ - 100.00')
        self.assertEquals(transactions_2.store.balance, 900)
        self.assertEquals(transactions_2.store.balance_display, 'R$  900.00')
        self.assertEquals(transactions_2.store.transactions_count, 2)
