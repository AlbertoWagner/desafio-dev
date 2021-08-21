
from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    path('', views.StoresListView.as_view(), name='store-list'),

]
