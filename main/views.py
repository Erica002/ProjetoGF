from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Despesa, Categoria, Renda, Wishlist
from .forms import CategoriaForm, DespesasUpdateForm, RendaForm, WishForm, DespesaForm
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

# FUNÇÕES RELACIONADAS A DESPESAS
@login_required(login_url="/autenticacao/login")
def index(request):
    despesas = Despesa.objects.filter(user=request.user)
    rendas = Renda.objects.filter(user=request.user)
    paginator = Paginator(despesas, 7)
    numero_page = request.GET.get("page")
    obj_page = Paginator.get_page(paginator, numero_page)
    valordespesas = 0
    valorreceita = 0
    valorsaldo = 0

    for despesa in despesas:
        valordespesas += despesa.valor_despesa
    for renda in rendas:
        valorreceita += renda.valor_renda

    valorsaldo = valorreceita - valordespesas
    # dicionário
    context = {
        "despesas": despesas,
        "obj_page": obj_page,
        "rendas": rendas,
        "valordespesas": valordespesas,
        "valorreceita": valorreceita,
        "valorsaldo": valorsaldo,
    }
    return render(request, "gastos/index.html", context)


@method_decorator(login_required, name="dispatch")
class CreateGastoView(CreateView):
    model = Despesa
    form_class = DespesaForm
    template_name = "gastos/gasto_form.html"

    def get_form_kwargs(self):
        kwargs = super(CreateGastoView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect("/")


@method_decorator(login_required, name="dispatch")
class GastoUpdateView(UpdateView):
    model = Despesa
    form_class = DespesasUpdateForm
    template_name = "gastos/gasto_form.html"
    success_url = "/"

    def get_form_kwargs(self):
        kwargs = super(GastoUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


@method_decorator(login_required, name="dispatch")
class DeleteGastoView(DeleteView):
    model = Despesa
    success_url = "/"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class CreateCategoriaView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "gastos/categoria_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect("list-categoria")


@method_decorator(login_required, name="dispatch")
class UpdateCategoriaView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "gastos/categoria_form.html"
    success_url = "/list-categoria"


@login_required(login_url="/autenticacao/login")
def list_categoria(request):
    categorias = Categoria.objects.filter(user=request.user)
    paginator = Paginator(categorias, 8)
    numero_page = request.GET.get("page")
    obj_page = Paginator.get_page(paginator, numero_page)
    # dicionário
    context = {"categorias": categorias, "obj_page": obj_page}
    return render(request, "gastos/list-categoria.html", context)


@method_decorator(login_required, name="dispatch")
class DeleteCategoriaView(DeleteView):
    model = Categoria
    success_url = "/list-categoria"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# FUNÇÕES RELACIONADAS A RENDA
@login_required(login_url="/autenticacao/login")
def list_ganho(request):
    ganho = Renda.objects.filter(user=request.user)
    despesas = Despesa.objects.filter(user=request.user)
    paginator = Paginator(ganho, 8)
    numero_page = request.GET.get("page")
    obj_page = Paginator.get_page(paginator, numero_page)
    valordespesas = 0
    valorreceita = 0
    valorsaldo = 0

    for despesa in despesas:
        valordespesas += despesa.valor_despesa
    for renda in ganho:
        valorreceita += renda.valor_renda

    valorsaldo = valorreceita - valordespesas
    # dicionário
    context = {
        "ganho": ganho,
        "obj_page": obj_page,
        "despesas": despesas,
        "valorreceita": valorreceita,
        "valorsaldo": valorsaldo,
    }
    return render(request, "ganhos/list-ganhos.html", context)


@method_decorator(login_required, name="dispatch")
class CreateRendaView(CreateView):
    model = Renda
    form_class = RendaForm
    template_name = "ganhos/ganho_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect("list-ganhos")


@method_decorator(login_required, name="dispatch")
class UpdateRendaView(UpdateView):
    model = Renda
    form_class = RendaForm
    template_name = "ganhos/ganho_form.html"
    success_url = "/list-ganhos"


@method_decorator(login_required, name="dispatch")
class DeleteRendaView(DeleteView):
    model = Renda
    success_url = "/list-ganhos"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# GRÁFICOS DESPESAS
@login_required(login_url="/autenticacao/login")
def grafico_por_categoria(request):
    labels = []
    data = []

    queryset = (
        Despesa.objects.values("categoria__nome")
        .annotate(categoria_val=Sum("valor_despesa"))
        .order_by("-categoria_val")
        .filter(user=request.user)
    )
    for entry in queryset:
        labels.append(entry["categoria__nome"])
        data.append(entry["categoria_val"])

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )


@login_required(login_url="/autenticacao/login")
def grafico_despesas_por_mes(request):
    labels = []
    data = []

    queryset = (
        Despesa.objects.values("data__month")
        .annotate(renda_val=Sum("valor_despesa"))
        .order_by("data__month")
        .filter(user=request.user)
    )
    for entry in queryset:
        labels.append(entry["data__month"])
        data.append(entry["renda_val"])

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )


@method_decorator(login_required, name="dispatch")
class MostraGraficoMensalView(ListView):
    model = Despesa
    template_name = "gastos/grafico-mensal.html"


@login_required(login_url="/autenticacao/login")
def grafico_despesas_por_ano(request):
    labels = []
    data = []

    queryset = (
        Despesa.objects.values("data__year")
        .annotate(renda_val=Sum("valor_despesa"))
        .order_by("data__year")
        .filter(user=request.user)
    )
    for entry in queryset:
        labels.append(entry["data__year"])
        data.append(entry["renda_val"])

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )


@method_decorator(login_required, name="dispatch")
class MostraGraficoAnualView(ListView):
    model = Despesa
    template_name = "gastos/grafico-anual.html"


# GRÁFICOS RECEITA
@login_required(login_url="/autenticacao/login")
def grafico_renda_por_mes(request):
    labels = []
    data = []

    queryset = (
        Renda.objects.values("data__month")
        .annotate(renda_val=Sum("valor_renda"))
        .order_by("data__month")
        .filter(user=request.user)
    )
    for entry in queryset:
        labels.append(entry["data__month"])
        data.append(entry["renda_val"])

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )


@login_required(login_url="/autenticacao/login")
def grafico_renda_por_ano(request):
    labels = []
    data = []

    queryset = (
        Renda.objects.values("data__year")
        .annotate(renda_val=Sum("valor_renda"))
        .order_by("data__year")
        .filter(user=request.user)
    )
    for entry in queryset:
        labels.append(entry["data__year"])
        data.append(entry["renda_val"])

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )


@method_decorator(login_required, name="dispatch")
class MostraGraficoRendaAnualView(ListView):
    model = Renda
    template_name = "ganhos/grafico-renda-anual.html"


# LISTA DE DESEJOS
@login_required(login_url="/autenticacao/login")
def list_wish(request):
    wishes = Wishlist.objects.filter(user=request.user)
    paginator = Paginator(wishes, 8)
    numero_page = request.GET.get("page")
    obj_page = Paginator.get_page(paginator, numero_page)

    # dicionário
    context = {
        "wishes": wishes,
        "obj_page": obj_page,
    }
    return render(request, "lista/list-wish.html", context)


@method_decorator(login_required, name="dispatch")
class WishCreateView(CreateView):
    model = Wishlist
    form_class = WishForm
    template_name = "lista/wish_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect("list-wish")


@method_decorator(login_required, name="dispatch")
class UpdateWishView(UpdateView):
    model = Wishlist
    form_class = WishForm
    template_name = "lista/wish_form.html"
    success_url = "/list-wish"


@method_decorator(login_required, name="dispatch")
class DeleteWishView(DeleteView):
    model = Wishlist
    success_url = "/list-wish"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


@login_required(login_url="/autenticacao/login")
def wish_delete(request, id):
    wish = Wishlist.objects.get(id=id)
    try:
        wish.delete()
    except:
        pass
    return redirect("list-wish")
