
from django.forms import ModelForm
from .models import Expense,Income

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ('name','amount','category')

class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ('income_name','income_amount','income_category')
        