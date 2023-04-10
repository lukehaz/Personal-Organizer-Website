from django import forms
from django.contrib.auth.models import User
from django.core import validators
from Budget.models import BudgetCategory, Budget

class BudgetEntryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size': 80}))
    category = forms.ModelChoiceField(queryset = BudgetCategory.objects.all())
    projected = forms.IntegerField(validators=[validators.MinValueValidator(0)])
    actual = forms.IntegerField(validators=[validators.MinValueValidator(0)])
    class Meta():
        model = Budget
        fields = ('description', 'category', 'projected', 'actual')
