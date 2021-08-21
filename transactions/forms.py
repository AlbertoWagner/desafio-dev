from django.forms import ModelForm, forms

from transactions.models import Transaction
from transactions.validator import validate_file_extension


class TransactionForm(ModelForm):
    file = forms.FileField(label='Txt', validators=[validate_file_extension])

    class Meta:
        fields = ('file',)
        model = Transaction

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
