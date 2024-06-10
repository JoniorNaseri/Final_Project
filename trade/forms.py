from django import forms
from .models import Trade


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = '__all__'


class LotForm(forms.Form):
    amount = forms.IntegerField()
    loss_dollar = forms.IntegerField()