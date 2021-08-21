
from django.urls import path
from . import views

app_name = "transactions"
urlpatterns = [
    path('', views.TransactionFormView.as_view(), name='action'),
    path('list/<store_id>', views.TransactionListView.as_view(), name='transaction-list'),

]
