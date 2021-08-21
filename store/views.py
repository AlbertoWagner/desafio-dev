
from django.views.generic import ListView

# Create your views here.
from store.models import Stores


class StoresListView(ListView):
    template_name = 'store/store_list.html'
    model = Stores
    paginate_by = 100