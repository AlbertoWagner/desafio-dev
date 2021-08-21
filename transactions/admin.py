from django.contrib import admin
from transactions.models import TransactionType, Transaction

admin.site.register(TransactionType)
admin.site.register(Transaction)
