from django.urls import path
from . import views

urlpatterns = [
    # Despesas
    path("", views.index, name="main"),
    path("add-gasto", views.CreateGastoView.as_view(), name="add-gasto"),
    path("add-categoria", views.add_categoria, name="add-categoria"),
    path("update-gasto/<int:id>", views.gasto_update, name="update-gasto"),
    path("delete-gasto/<int:id>", views.gasto_delete, name="delete-gasto"),
    path("list-categoria", views.list_categoria, name="list-categoria"),
    path("update-categoria/<int:id>", views.categoria_update, name="update-categoria"),
    path("delete-categoria/<int:id>", views.categoria_delete, name="delete-categoria"),
    # Receita
    path("list-ganhos", views.list_ganho, name="list-ganhos"),
    path("add-ganho", views.add_ganho, name="add-ganho"),
    path("update-ganhos/<int:id>", views.ganho_update, name="update-ganhos"),
    path("delete-ganhos/<int:id>", views.ganho_delete, name="delete-ganhos"),
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
    path("grafico-mensal", views.mostra_grafico_mensal, name="grafico-mensal"),
    path(
        "grafico_despesas_por_ano/",
        views.grafico_despesas_por_ano,
        name="grafico_despesas_por_ano",
    ),
    path("grafico-anual", views.mostra_grafico_anual, name="grafico-anual"),
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
    path("grafico-renda-anual", views.mostra_renda_anual, name="grafico-renda-anual"),
    # WISHLIST
    path("list-wish", views.list_wish, name="list-wish"),
    path("add-wish", views.add_wish, name="add-wish"),
    path("update-wish/<int:id>", views.wish_update, name="update-wish"),
    path("delete-wish/<int:id>", views.wish_delete, name="delete-wish"),
]
