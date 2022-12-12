from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages, auth
# Create your views here.

class CadastrarUsuarioView(View):
    def get(self, request):
        return render(request, 'autenticacao/cadastro-usuario.html')

    def post(self, request):
        # Pegar os dados do usuário, validar e criar conta
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # mantém os campos preenchidos antes da senha, para o caso de ser muito curta e disparar o alerta.
        context = {
            'fieldValue': request.POST 
        }
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, 'A senha precisa ter pelo menos 8 caracteres')
                    return render(request, 'autenticacao/cadastro-usuario.html', context)

                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Usuário cadastrado com sucesso!')
                return render(request, 'autenticacao/cadastro-usuario.html')

        return render(request, 'autenticacao/cadastro-usuario.html')

class ValidarUsuarioView(View):
    def post(self, request):
        # Transforma os dados em um dicionário no formato JSON
        data = json.loads(request.body)
        # Pega o nome de usuário do dicionário
        username = data['username'] 
        # Verifica se o nome do usuário contém algum caractére alphanumérico. 
        if not str(username).isalnum():
            return JsonResponse({'error_usuario': 'O nome de usuário deve ser composto de apenas letras e/ou números)'}, status=400)
        # Verifica se o usuário está cadastrado no banco de dados.
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error_usuario': 'Esse nome de usuário já existe'}, status=409)
        return JsonResponse({'usuario_valido': True})

class ValidarEmailView(View):
    def post(self, request):
        data = json.loads(request.body) 
        email = data['email'] 
        if not validate_email(email):
            return JsonResponse({'error_email': 'Formato de email inserido é inválido. Tente novamente.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error_email': 'O email inserido já existe. Por favor escolha outro.'}, status=409)
        # else
        return JsonResponse({'email_valido': True})

class LoginUsuarioView(View):
    def get(self, request):
        return render(request, 'autenticacao/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Olá, '+ user.username)
                    
                    return redirect('main')

                messages.error(request, 'O nome de usuário inserido está inativo.')
                return render(request, 'autenticacao/login.html')

            messages.error(request, 'Nome de usuário ou senha incorreta. Tente novamente')    
            return render(request, 'autenticacao/login.html') 
        


class LogoutUsuarioView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request, 'Você saiu da sua conta')
        return redirect('login')
    