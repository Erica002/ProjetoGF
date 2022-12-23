from django.forms import ModelForm
from .models import Categoria, Renda, Despesa, Wishlist
from django import forms

from main import models


class DatePickerInput(forms.DateInput):
    input_type = "date"


class TimePickerInput(forms.TimeInput):
    input_type = "time"


class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome"]


class DespesaForm(ModelForm):
    class Meta:
        model = Despesa
        fields = ("detalhes", "valor_despesa", "data", "categoria", "forma_pagamento")
        widgets = {
            "data": forms.TimeInput(attrs={"type": "date"}),
        }

    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super(DespesaForm, self).__init__(*args, **kwargs)
        self.fields["categoria"].queryset = self.fields["categoria"].queryset.filter(
            usuario=request.user
        )


class RendaForm(ModelForm):
    class Meta:
        model = Renda
        fields = ["detalhes", "valor_renda", "origem", "data"]
        widgets = {
            "data": forms.TimeInput(attrs={"type": "date"}),
        }


class WishForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = ["detalhes", "valor_necessario", "valor_salvo", "data"]
        widgets = {
            "data": forms.TimeInput(attrs={"type": "date"}),
        }
