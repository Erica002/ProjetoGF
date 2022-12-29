from django.forms import ModelForm
from .models import Categoria, Renda, Despesa, Wishlist
from django import forms


class DatePickerInput(forms.DateInput):
    input_type = "date"


class TimePickerInput(forms.TimeInput):
    input_type = "time"


class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Categoria
        fields = ["nome"]


class DespesaForm(ModelForm):
    class Meta:
        model = Despesa
        fields = (
            "detalhes",
            "valor_despesa",
            "data",
            "categoria",
            "forma_pagamento",
        )
        widgets = {
            "detalhes": forms.Textarea(attrs={"class": "form-control", "type": "text"}),
            "valor_despesa": forms.TextInput(
                attrs={"class": "form-control", "type": "text"}
            ),
            "forma_pagamento": forms.Select(
                attrs={"class": "form-control", "type": "text"}
            ),
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super(DespesaForm, self).__init__(*args, **kwargs)
        self.fields["categoria"].queryset = self.fields["categoria"].queryset.filter(
            user=request.user
        )


class DespesasUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super(DespesasUpdateForm, self).__init__(*args, **kwargs)
        self.fields["categoria"].queryset = self.fields["categoria"].queryset.filter(
            user=request.user
        )
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Despesa
        fields = [
            "detalhes",
            "valor_despesa",
            "data",
            "categoria",
            "forma_pagamento",
        ]

        widgets = {
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class RendaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RendaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Renda
        fields = ["detalhes", "valor_renda", "origem", "data"]

        widgets = {
            "data": forms.TimeInput(attrs={"type": "date"}),
        }


class WishForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WishForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Wishlist
        fields = ["detalhes", "valor_necessario", "valor_salvo", "data"]
        widgets = {
            "data": forms.TimeInput(attrs={"type": "date"}),
        }
