from django import forms
from .models import ItemPrice

class ItemPriceForm(forms.ModelForm):
    class Meta:
        model = ItemPrice
        fields = ['title', 'price']
