from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_types_all(sender, **kwargs):
    from transactions.models import TransactionType
    description = ['Débito', 'Boleto', 'Financiamento', 'Crédito', 'Recebimento Empréstimo', 'Vendas',
                   'Recebimento TED', 'Recebimento DOC', 'Aluguel']
    choices = [1, 2, 2, 1, 1, 1, 1, 1, 2]

    for index in range(len(description)):
        TransactionType.objects.update_or_create(type_transactions=index + 1, description=description[index],
                                                 nature=choices[index],
                                                 signal=choices[index])


class TransactionConfig(AppConfig):
    """App settings"""

    name = "transactions"

    def ready(self):
        post_migrate.connect(create_types_all, sender=self)
        import transactions.signals
