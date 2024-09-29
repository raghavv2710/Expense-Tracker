from django import forms
from .models import Expense
from django.utils import timezone

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'category', 'date']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': timezone.now().date().strftime('%Y-%m-%d'),
                'max': (timezone.now() + timezone.timedelta(days=365)).date().strftime('%Y-%m-%d')
            }),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError("The date cannot be in the past.")
        return date

