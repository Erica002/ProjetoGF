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
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# FUNÇÕES RELACIONADAS A DESPESAS
class MeusGastosView(LoginRequiredMixin, View):
    login_url = "/autenticacao/login"

    def get(self, request):
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


class CreateGastoView(LoginRequiredMixin, CreateView):
    login_url = "/autenticacao/login"
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


class GastoUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/autenticacao/login"
    model = Despesa
    form_class = DespesasUpdateForm
    template_name = "gastos/gasto_form.html"
    success_url = "/"

    def get_form_kwargs(self):
        kwargs = super(GastoUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class DeleteGastoView(LoginRequiredMixin, DeleteView):
    login_url = "/autenticacao/login"
    model = Despesa
    success_url = "/"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CreateCategoriaView(LoginRequiredMixin, CreateView):
    login_url = "/autenticacao/login"
    model = Categoria
    form_class = CategoriaForm
    template_name = "gastos/categoria_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect("list-categoria")


class UpdateCategoriaView(LoginRequiredMixin, UpdateView):
    login_url = "/autenticacao/login"
    model = Categoria
    form_class = CategoriaForm
    template_name = "gastos/categoria_form.html"
    success_url = "/list-categoria"


class ListarCategoriaView(LoginRequiredMixin, View):
    login_url = "/autenticacao/login"

    def get(self, request):
        categorias = Categoria.objects.filter(user=request.user)
        paginator = Paginator(categorias, 8)
        numero_page = request.GET.get("page")
        obj_page = Paginator.get_page(paginator, numero_page)
        # dicionário
        context = {"categorias": categorias, "obj_page": obj_page}
        return render(request, "gastos/list-categoria.html", context)


class DeleteCategoriaView(LoginRequiredMixin, DeleteView):
    login_url = "/autenticacao/login"
    model = Categoria
    success_url = "/list-categoria"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ListagemGanhoView(LoginRequiredMixin, View):
    login_url = "/autenticacao/login"

    def get(self, request):
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


class CreateRendaView(LoginRequiredMixin, CreateView):
    login_url = "/autenticacao/login"
    model = Renda
    form_class = RendaForm
    template_name = "ganhos/ganho_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect("list-ganhos")


class UpdateRendaView(LoginRequiredMixin, UpdateView):
    login_url = "/autenticacao/login"
    model = Renda
    form_class = RendaForm
    template_name = "ganhos/ganho_form.html"
    success_url = "/list-ganhos"


class DeleteRendaView(LoginRequiredMixin, DeleteView):
    login_url = "/autenticacao/login"
    model = Renda
    success_url = "/list-ganhos"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# GRÁFICOS DESPESAS
class grafico_por_categoria(LoginRequiredMixin, View):
    login_url = "/autenticacao/login"

    def get(self, request):
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


class grafico_despesas_por_mes(LoginRequiredMixin, View):
    login_url = "/autenticacao/login"

    def get(self, request):
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


class MostraGraficoMensalView(LoginRequiredMixin, ListView):
    login_url = "/autenticacao/login"
    model = Despesa
    template_name = "gastos/grafico-mensal.html"


class grafico_despesas_por_ano(LoginRequiredMixin, View):
    login_url = "/autenticacao/login"

    def get(self, request):
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


class MostraGraficoAnualView(LoginRequiredMixin, ListView):
    login_url = "/autenticacao/login"
    model = Despesa
    template_name = "gastos/grafico-anual.html"


# GRÁFICOS RECEITA
class grafico_renda_por_mes(LoginRequiredMixin, View):
    login_url = "/autenticacao/login"

    def get(self, request):
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


class grafico_renda_por_ano(LoginRequiredMixin, View):
    login_url = "/autenticacao/login"

    def get(self, request):
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


class MostraGraficoRendaAnualView(LoginRequiredMixin, ListView):
    login_url = "/autenticacao/login"
    model = Renda
    template_name = "ganhos/grafico-renda-anual.html"


# LISTA DE DESEJOS
class ListagemWishesView(LoginRequiredMixin, View):
    login_url = "/autenticacao/login"

    def get(self, request):
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


class WishCreateView(LoginRequiredMixin, CreateView):
    login_url = "/autenticacao/login"
    model = Wishlist
    form_class = WishForm
    template_name = "lista/wish_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect("list-wish")


class UpdateWishView(LoginRequiredMixin, UpdateView):
    login_url = "/autenticacao/login"
    model = Wishlist
    form_class = WishForm
    template_name = "lista/wish_form.html"
    success_url = "/list-wish"


class DeleteWishView(LoginRequiredMixin, DeleteView):
    login_url = "/autenticacao/login"
    model = Wishlist
    success_url = "/list-wish"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
