from django.urls import path
from . import views

urlpatterns = [
    # Despesas
    path("", views.index, name="main"),
    path("add-gasto", views.CreateGastoView.as_view(), name="gasto_form"),
    path("add-categoria", views.CreateCategoriaView.as_view(), name="categoria_form"),
    path("update-gasto/<int:pk>", views.GastoUpdateView.as_view(), name="gasto_form"),
    path("delete-gasto/<int:pk>", views.DeleteGastoView.as_view(), name="delete-gasto"),
    path("list-categoria", views.list_categoria, name="list-categoria"),
    path(
        "update-categoria/<int:pk>",
        views.UpdateCategoriaView.as_view(),
        name="categoria_form",
    ),
    path(
        "delete-categoria/<int:pk>",
        views.DeleteCategoriaView.as_view(),
        name="delete-categoria",
    ),
    # Receita
    path("list-ganhos", views.list_ganho, name="list-ganhos"),
    path("add-ganho", views.CreateRendaView.as_view(), name="ganho_form"),
    path("update-ganhos/<int:pk>", views.UpdateRendaView.as_view(), name="ganho_form"),
    path(
        "delete-ganhos/<int:pk>", views.DeleteRendaView.as_view(), name="delete-ganhos"
    ),
    # Gráficos
    path(
        "grafico_por_categoria/",
        views.grafico_por_categoria,
        name="grafico_por_categoria",
    ),
    path(
        "grafico_despesas_por_mes/",
        views.grafico_despesas_por_mes,
        name="grafico_despesas_por_mes",
    ),
    path(
        "grafico-mensal", views.MostraGraficoMensalView.as_view(), name="grafico-mensal"
    ),
    path(
        "grafico_despesas_por_ano/",
        views.grafico_despesas_por_ano,
        name="grafico_despesas_por_ano",
    ),
    path("grafico-anual", views.MostraGraficoAnualView.as_view(), name="grafico-anual"),
    path(
        "grafico_renda_por_mes/",
        views.grafico_renda_por_mes,
        name="grafico_renda_por_mes",
    ),
    path(
        "grafico_renda_por_ano/",
        views.grafico_renda_por_ano,
        name="grafico_renda_por_ano",
    ),
    path(
        "grafico-renda-anual",
        views.MostraGraficoRendaAnualView.as_view(),
        name="grafico-renda-anual",
    ),
    # WISHLIST
    path("list-wish", views.list_wish, name="list-wish"),
    path("add-wish", views.WishCreateView.as_view(), name="wish_form"),
    path("update-wish/<int:pk>", views.UpdateWishView.as_view(), name="wish_form"),
    path("delete-wish/<int:pk>", views.DeleteWishView.as_view(), name="delete-wish"),
]
