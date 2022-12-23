from .views import (
    CadastrarUsuarioView,
    ValidarUsuarioView,
    ValidarEmailView,
    LoginUsuarioView,
    LogoutUsuarioView,
)
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("cadastro-usuario", CadastrarUsuarioView.as_view(), name="cadastro-usuario"),
    path(
        "valida_usuario",
        csrf_exempt(ValidarUsuarioView.as_view()),
        name="valida_usuario",
    ),
    path(
        "validacao_email",
        csrf_exempt(ValidarEmailView.as_view()),
        name="validacao_email",
    ),
    path("login", LoginUsuarioView.as_view(), name="login"),
    path("logout", LogoutUsuarioView.as_view(), name="logout"),
]
