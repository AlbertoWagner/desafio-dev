import datetime

from django.urls import reverse
from django.db import transaction
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from store.models import Stores
from transactions.forms import TransactionForm
from transactions.models import TransactionType, Transaction


class TransactionFormView(CreateView):
    template_name = 'transactions/transactions_forms.html'
    form_class = TransactionForm

    success_url = 'store:store-list'
    success_message = "Sucesso na importação!!"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                with transaction.atomic():
                    for linha in self.request.FILES['file'].readlines():
                        texto = linha.decode('utf-8')
                        if texto != '\n':
                            data = dict()
                            transactions_type = TransactionType.objects.get(type_transactions=texto[0])
                            store, create = Stores.objects.get_or_create(
                                **{'store_owner': texto[48:62].strip(), 'name': texto[62:81].strip().replace('\n', '')})
                            data['transactions_type_id'] = transactions_type.id
                            data['date'] = datetime.datetime.strptime(f"{texto[1:5]}-{texto[5:7]}-{texto[7:9]}",
                                                                      '%Y-%m-%d').date()
                            data['value'] = float(texto[9:19]) / 100
                            data['cpf'] = texto[19:30]
                            data['card'] = texto[30:42]
                            data['time'] = datetime.datetime.strptime(f"{texto[42:44]}:{texto[44:46]}:{texto[46:48]}",
                                                                      '%H:%M:%S').time()
                            data['store_id'] = store.id
                            Transaction.objects.get_or_create(**data)
                    messages.success(request, self.success_message)

                return HttpResponseRedirect(reverse(self.success_url))
            except Exception as e:
                messages.error(request, "Erro ao importa arquivo")
                return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})


class TransactionListView(ListView):
    template_name = 'transactions/transactions_list.html'
    model = Transaction
    title = 'Transações/ Lojas'

    def get_store(self):
        return Stores.objects.get(pk=self.kwargs.get('store_id'))

    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        context["store"] = self.get_store()
        return context

    def get_queryset(self):
        return Transaction.objects.filter(store=self.get_store())
