from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Despesa, Categoria, Renda, Wishlist
from .forms import CategoriaForm, RendaForm, WishForm
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse

# FUNÇÕES RELACIONADAS A DESPESAS
@login_required(login_url='/autenticacao/login')
def index(request):
    despesas = Despesa.objects.filter(usuario=request.user) 
    rendas = Renda.objects.filter(usuario=request.user)
    paginator = Paginator(despesas, 8)
    numero_page = request.GET.get('page')
    obj_page = Paginator.get_page(paginator, numero_page) 
    valordespesas = 0
    valorreceita = 0
    valorsaldo = 0
    
    for despesa in despesas:
        valordespesas += despesa.valor_despesa
    for renda in rendas:
        valorreceita += renda.valor_renda
    
    valorsaldo =  valorreceita - valordespesas
    #dicionário
    context = {
        'despesas': despesas,
        'obj_page': obj_page,
        'rendas': rendas,
        'valordespesas': valordespesas,
        'valorreceita': valorreceita,
        'valorsaldo': valorsaldo
    }
    return render(request, 'gastos/index.html',context)

@login_required(login_url='/autenticacao/login')
def add_gasto(request):
    categorias = Categoria.objects.filter(usuario=request.user)
    despesas = Despesa.objects.all()
    context={
        'categorias': categorias,
        'despesas': despesas,
        'valor': request.POST
    }
    if request.method == 'GET':
        return render(request, 'gastos/add-gasto.html', context)

    if request.method == 'POST':
        detalhes = request.POST['detalhes']
        valor_despesa = request.POST['valor_despesa']
        categoria = request.POST['categoria']
        data = request.POST['data']

    Despesa.objects.create(usuario=request.user, detalhes=detalhes, valor_despesa=valor_despesa,categoria=Categoria.objects.get(nome=categoria), data=data)    

    return redirect('main')

@login_required(login_url='/autenticacao/login')
def add_categoria(request):
    if request.method == "POST":  
        form = CategoriaForm(request.POST)  
        if form.is_valid():  
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            #model = form.instance
            return redirect('list-categoria')
        return render(request, 'gastos/add-categoria.html',{"form": form})     
    form = CategoriaForm()  
    return render(request, 'gastos/add-categoria.html',{'form':form}) 


@login_required(login_url='/autenticacao/login')
def gasto_update(request, id):
    gasto = Despesa.objects.get(id=id)
    categorias = Categoria.objects.filter(usuario=request.user)
    context={
        'gasto': gasto,
        'valor': gasto,
        'categorias': categorias,
    }
    if request.method=='GET':
        return render(request, 'gastos/update-gasto.html', context)
    if request.method=='POST':
        detalhes = request.POST['detalhes']
        valor_despesa = request.POST['valor_despesa']
        categoria = request.POST['categoria']
        data = request.POST['data']

        gasto.usuario=request.user 
        gasto.detalhes=detalhes 
        gasto.valor_despesa=valor_despesa
        gasto.categoria=Categoria.objects.get(nome=categoria) 
        gasto.data=data
        gasto.save()

        return redirect('main')
 

@login_required(login_url='/autenticacao/login')
def gasto_delete(request, id):
    gasto = Despesa.objects.get(id=id)
    try:
        gasto.delete()
    except:
        pass
    return redirect('main')

@login_required(login_url='/autenticacao/login')
def list_categoria(request):
    categorias = Categoria.objects.filter(usuario=request.user)  
    paginator = Paginator(categorias, 8)
    numero_page = request.GET.get('page')
    obj_page = Paginator.get_page(paginator, numero_page) 
    #dicionário
    context = {
        'categorias': categorias,
        'obj_page': obj_page
    } 
    return render(request, 'gastos/list-categoria.html',context)

@login_required(login_url='/autenticacao/login')
def categoria_update(request, id):  
    categoria = Categoria.objects.get(id=id)
    form = CategoriaForm(initial={'nome': categoria.nome})
    if request.method == "POST":  
        form = CategoriaForm(request.POST, instance=categoria)  
        if form.is_valid():  
            try:  
                form.save() 
                model = form.instance
                return redirect('list-categoria')  
            except Exception as e: 
                pass    
    return render(request,'gastos/update-categoria.html',{'form':form})  
 

@login_required(login_url='/autenticacao/login')
def categoria_delete(request, id):
    categoria = Categoria.objects.get(id=id)
    try:
        categoria.delete()
    except:
        pass
    return redirect('list-categoria')

# FUNÇÕES RELACIONADAS A RENDA
@login_required(login_url='/autenticacao/login')
def list_ganho(request):
    ganho = Renda.objects.filter(usuario=request.user) 
    despesas = Despesa.objects.filter(usuario=request.user)
    paginator = Paginator(ganho, 8)
    numero_page = request.GET.get('page')
    obj_page = Paginator.get_page(paginator, numero_page) 
    valordespesas = 0
    valorreceita = 0
    valorsaldo = 0
    
    for despesa in despesas:
        valordespesas += despesa.valor_despesa
    for renda in ganho:
        valorreceita += renda.valor_renda
    
    valorsaldo =  valorreceita - valordespesas
    #dicionário
    context = {
        'ganho': ganho,
        'obj_page': obj_page,
        'despesas': despesas,
        'valorreceita': valorreceita,
        'valorsaldo' : valorsaldo
    } 
    return render(request, 'ganhos/list-ganhos.html',context)


@login_required(login_url='/autenticacao/login')
def add_ganho(request):
    if request.method == "POST":  
        form = RendaForm(request.POST)  
        if form.is_valid():  
            ganho = form.save(commit=False)
            ganho.usuario = request.user
            ganho.save()
            #model = form.instance
            return redirect('list-ganhos')
        return render(request, 'ganhos/add-ganho.html',{"form": form})     
    form = RendaForm()  
    return render(request, 'ganhos/add-ganho.html',{'form':form}) 

@login_required(login_url='/autenticacao/login')
def ganho_update(request, id):  
    ganho = Renda.objects.get(id=id)
    form = RendaForm(initial={'detalhes': ganho.detalhes, 'valor_renda': ganho.valor_renda, 'data':ganho.data})
    if request.method == "POST":  
        form = RendaForm(request.POST, instance=ganho)  
        if form.is_valid():  
            try:  
                form.save() 
                model = form.instance
                return redirect('list-ganhos')  
            except Exception as e: 
                pass    
    return render(request,'ganhos/update-ganhos.html',{'form':form})  
 

@login_required(login_url='/autenticacao/login')
def ganho_delete(request, id):
    ganho = Renda.objects.get(id=id)
    try:
        ganho.delete()
    except:
        pass
    return redirect('list-ganhos')

#GRÁFICOS DESPESAS
@login_required(login_url='/autenticacao/login')
def grafico_por_categoria(request):
    labels = []
    data = []

    queryset = Despesa.objects.values('categoria__nome').annotate(categoria_val=Sum('valor_despesa')).order_by('-categoria_val').filter(usuario=request.user)
    for entry in queryset:
        labels.append(entry['categoria__nome'])
        data.append(entry['categoria_val'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required(login_url='/autenticacao/login')
def grafico_despesas_por_mes(request):
    labels = []
    data = []

    queryset = Despesa.objects.values('data__month').annotate(renda_val=Sum('valor_despesa')).order_by('data__month').filter(usuario=request.user)
    for entry in queryset:
        labels.append(entry['data__month'])
        data.append(entry['renda_val'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required(login_url='autenticacao/login')
def mostra_grafico_mensal(request):
    return render(request, 'gastos/grafico-mensal.html')


@login_required(login_url='/autenticacao/login')
def grafico_despesas_por_ano(request):
    labels = []
    data = []

    queryset = Despesa.objects.values('data__year').annotate(renda_val=Sum('valor_despesa')).order_by('data__year').filter(usuario=request.user)
    for entry in queryset:
        labels.append(entry['data__year'])
        data.append(entry['renda_val'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required(login_url='autenticacao/login')
def mostra_grafico_anual(request):
    return render(request, 'gastos/grafico-anual.html')

# GRÁFICOS RECEITA
@login_required(login_url='/autenticacao/login')
def grafico_renda_por_mes(request):
    labels = []
    data = []

    queryset = Renda.objects.values('data__month').annotate(renda_val=Sum('valor_renda')).order_by('data__month').filter(usuario=request.user)
    for entry in queryset:
        labels.append(entry['data__month'])
        data.append(entry['renda_val'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required(login_url='/autenticacao/login')
def grafico_renda_por_ano(request):
    labels = []
    data = []

    queryset = Renda.objects.values('data__year').annotate(renda_val=Sum('valor_renda')).order_by('data__year').filter(usuario=request.user)
    for entry in queryset:
        labels.append(entry['data__year'])
        data.append(entry['renda_val'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required(login_url='autenticacao/login')
def mostra_renda_anual(request):
    return render(request, 'ganhos/grafico-renda-anual.html')


# LISTA DE DESEJOS
@login_required(login_url='/autenticacao/login')
def list_wish(request):
    wishes = Wishlist.objects.filter(usuario=request.user)  
    paginator = Paginator(wishes, 8)
    numero_page = request.GET.get('page')
    obj_page = Paginator.get_page(paginator, numero_page) 
    
    #dicionário
    context = {
        'wishes': wishes,
        'obj_page': obj_page,
    } 
    return render(request, 'lista/list-wish.html',context)

@login_required(login_url='/autenticacao/login')
def add_wish(request):
    if request.method == "POST":  
        form = WishForm(request.POST)  
        if form.is_valid():  
            wish = form.save(commit=False)
            wish.usuario = request.user
            wish.save()
            return redirect('list-wish')
        return render(request, 'lista/add-wish.html',{"form": form})     
    form = WishForm()  
    return render(request, 'lista/add-wish.html',{'form':form}) 

@login_required(login_url='/autenticacao/login')
def wish_update(request, id):  
    wish = Wishlist.objects.get(id=id)
    form = WishForm(initial={'detalhes': wish.detalhes, 'valor_necessario': wish.valor_necessario, 'valor_salvo': wish.valor_salvo, 'data': wish.data})
    if request.method == "POST":  
        form = WishForm(request.POST, instance=wish)  
        if form.is_valid():  
            try:  
                form.save() 
                model = form.instance
                return redirect('list-wish')  
            except Exception as e: 
                pass    
    return render(request,'lista/update-wish.html',{'form':form})  
 

@login_required(login_url='/autenticacao/login')
def wish_delete(request, id):
    wish = Wishlist.objects.get(id=id)
    try:
        wish.delete()
    except:
        pass
    return redirect('list-wish')