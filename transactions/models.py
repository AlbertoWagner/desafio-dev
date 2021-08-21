from django.db import models
from transactions import choices
from transactions.validator import validaCpf


class TransactionType(models.Model):
    type = models.IntegerField()
    description = models.CharField(max_length=120)
    nature = models.IntegerField(choices=choices.C_TRANSACTION)
    signal = models.IntegerField(choices=choices.C_SIGNAL)

    class Meta:
        ordering = ['type']
        verbose_name = u'Transaction type'
        verbose_name_plural = u'Transactions types'
        db_table = 'transaction_type'

    def __str__(self):
        return f'Tipo : {self.type} {self.description}'


class Transaction(models.Model):
    cpf = models.CharField(max_length=11, validators=[validaCpf])
    value = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    card = models.CharField(max_length=120)
    type = models.ForeignKey("transactions.TransactionType", on_delete=models.PROTECT, related_name="transactions")
    store = models.ForeignKey("store.Stores", on_delete=models.PROTECT, related_name="stores")

    class Meta:
        ordering = ['date']
        verbose_name = u'Transaction'
        verbose_name_plural = u'Transactions'
        db_table = 'transaction'

    @property
    def get_display_value(self):
        if self.type.signal == choices.SUM:
            return f'R$ {self.value :.2f}'
        else:
            return f'R$ - {self.value :.2f}'

    @property
    def get_display_status(self):
        if self.type.signal == choices.SUM:
            return 'breadcrumb-item table-success'
        else:
            return 'breadcrumb-item table-danger'
