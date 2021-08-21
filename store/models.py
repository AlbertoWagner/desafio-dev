from django.db import models

from transactions.models import Transaction
from transactions import choices


class Stores(models.Model):
    name = models.CharField(max_length=120)
    store_owner = models.CharField(max_length=120)

    class Meta:
        ordering = ['store_owner']
        verbose_name = u'Store'
        verbose_name_plural = u'Stores'
        db_table = 'stores'

    @property
    def balance(self):
        from django.db.models import Sum
        entrada = Transaction.objects.filter(store=self, type__signal=choices.SUM).aggregate(
            total=Sum('value')).get('total', 0) or 0
        saida = Transaction.objects.filter(store=self, type__signal=choices.SUBTRACTION).aggregate(
            total=Sum('value')).get('total', 0) or 0
        return entrada - saida

    @property
    def balance_display(self):
        return f'R$  {self.balance :.2f}'

    @property
    def transactions_count(self):
        return Transaction.objects.filter(store=self).count()

    @property
    def get_display_status(self):
        if self.balance > 0:
            return 'breadcrumb-item table-success'
        else:
            return 'breadcrumb-item table-danger'
