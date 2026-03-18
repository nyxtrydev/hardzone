from django import forms
from .models import Expense, ExpenseCategory

class ExpenseForm(forms.ModelForm):
    class ImageForm(forms.Form):
        bill = forms.FileField()

    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description', 'bill']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'bill': forms.FileInput(attrs={'class': 'form-control'}),
        }
