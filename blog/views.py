from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, resolve_url, redirect
from django.views.generic import CreateView, UpdateView
from django.utils import timezone
from django.forms import inlineformset_factory
from django.views.decorators.csrf import csrf_protect
from .models import Produto,Estoque, EstoqueEntrada, EstoqueSaida, EstoqueItens, Parceiro
from .form import ProdutoForm, EstoqueForm, EstoqueItensForm, ParceiroForm


@login_required(login_url='/login/')
def index(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
    #return render(request, 'blog/post_list.html', {'posts': posts})
    return render(request, 'blog/index.html')
    
def post_list (request):
    return render(request, 'blog/post_list.html')

def produto_list (request):
    template_name = 'blog/produto_list.html'
    objects = Produto.objects.all()
    search =   request.GET.get('search')
    if search:
        objects = objects.filter(produto__icontains=search)
    context = {'object_list': objects}
    return render( request, template_name, context)

def detail_prod (request, pk):
    template_name = 'blog/detail_prod.html'
    codigoP = Produto.objects.get(pk=pk)
    context = {'object': codigoP}
    return render( request, template_name, context)

def produto_add(request):
    template_name= 'blog/form_prod.html'
    return render (request, template_name)

def produto_submit(request):
    importado = request.POST.get('importado')
    ncm = request.POST.get('ncm')
    produto = request.POST.get('produto')
    preco = request.POST.get('preco')
    estoque = request.POST.get('estoque')
    estoque_minimo = request.POST.get('estoque_minimo')
    tipo_produto = request.POST.get('tipo_parceiro')
    codigoP = request.POST.get('cod')
    prod = Produto.objects.create( importado=importado, ncm=ncm, produto=produto,preco=preco,
    estoque=estoque, estoque_minimo=estoque_minimo, tipo_produto=tipo_produto,)
    url = '/'
    return redirect(url)

class ProdutoCreate(CreateView):
    model = Produto
    template_name = 'blog/form_prod.html'
    form_class = ProdutoForm

class ProdutoUpdate(UpdateView):
    model = Produto
    template_name = 'blog/form_prod.html'
    form_class = ProdutoForm

def ent_estoque (request):
    template_name = 'blog/estoque_list.html'
    objects = EstoqueEntrada.objects.all()
    search =   request.GET.get('search')
    if search:
        objects = objects.filter(nf__icontains=search)
    context = {'object_list':objects,'titulo':'Entrada','url_add':'blog:ent_estoque_form'}

    return render (request, template_name, context) 
    
def ent_estoque_detail (request, pk):
    template_name = 'blog/estoque_detail.html'
    obj = EstoqueEntrada.objects.get(pk=pk)
    context = {'object':obj, 'url_list':'blog:ent_estoque',}
    return render (request, template_name, context) 

def dar_baixa_estoque(form):
    # Pega os produtos a partir da instância do formulário (Estoque).
    produtos = form.estoques.all()
    for item in produtos:
        produto = Produto.objects.get(pk=item.produto.pk)
        produto.estoque = item.saldo
        produto.save()
    print('Estoque atualizado com sucesso.')

def estoque_add(request, template_name, movimento, url):
    estoque_form = Estoque()
    item_estoque_formset = inlineformset_factory(
    Estoque,
    EstoqueItens,
    form = EstoqueItensForm,
    extra = 0,
    can_delete = False,
    min_num = 1,
    validate_min = True,
    )
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance= estoque_form, prefix = 'main')
        formset = item_estoque_formset(request.POST, instance= estoque_form, prefix= 'estoque')
        if form.is_valid() and formset.is_valid():
            form = form.save(commit=False)
            form.funcionario = request.user
            form.movimento = movimento
            form.save()
            formset.save()
            dar_baixa_estoque(form)
            return {'pk': form.pk}
    else:
        form = EstoqueForm(instance= estoque_form, prefix = 'main')
        formset = item_estoque_formset(instance= estoque_form, prefix= 'estoque')
    context = {'form':form, 'formset':formset}
    return context

def ent_estoque_form (request):
    template_name = 'blog/ent_estoque_form.html'
    movimento = 'e'
    url = 'blog:ent_estoque_detail'
    context = estoque_add(request, template_name, movimento, url)
    if context.get('pk'):
        return HttpResponseRedirect(resolve_url(url, context.get( 'pk')))
    return render (request, template_name, context) 

def produto_json(request, pk):
    #''' Retorna o produto, id e estoque. '''
    produto = Produto.objects.filter(pk=pk)
    data = [item.to_dict_json() for item in produto]
    return JsonResponse({'data': data})

def sai_estoque_detail (request, pk):
    template_name = 'blog/estoque_detail.html'
    obj = EstoqueSaida.objects.get(pk=pk)
    context = {'object':obj, 'url_list':'blog:sai_estoque'}
    return render (request, template_name, context) 

def sai_estoque (request):
    template_name = 'blog/estoque_list.html'
    objects = EstoqueSaida.objects.all()
    search =   request.GET.get('search')
    if search:
        objects = objects.filter(nf__icontains=search)
    context = {'object_list':objects, 'titulo':'Saída', 'url_add':'blog:sai_estoque_form'}
    return render (request, template_name, context) 
  
def sai_estoque_form (request):
    template_name = 'blog/sai_estoque_form.html'
    movimento = 's'
    url = 'blog:sai_estoque_detail'
    context = estoque_add(request, template_name, movimento, url)
    if context.get('pk'):
        return HttpResponseRedirect(resolve_url(url, context.get( 'pk')))
    return render (request, template_name, context) 

def logout_user (request):
    logout (request)
    return redirect ('/login/')

def login_user (request):
    return render (request, 'blog/login.html')
csrf_protect
def submit_login (request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate (username = username, password = password)
        if user is not None:
            login (request, user)
            return redirect ('/')
        else:
            messages.error (request, 'Usuário ou senha Inválido. Tente novamente')
    return redirect ('/login/')

def parceiro_list (request):
    template_name = 'blog/parceiro_list.html'
    objects = Parceiro.objects.all()
    search =   request.GET.get('search')
    if search:
        objects = objects.filter(parceiro__icontains=search)
    context = {'object_lista': objects}
    return render( request, template_name, context)

def parceiro_detail (request, pk):
    template_name = 'blog/parceiro_detail.html'
    codigo = Parceiro.objects.get(pk=pk)
    context = {'object_par': codigo}
    return render( request, template_name, context)

def parceiro_add(request):
    template_name = 'blog/parceiro_form.html'
    return render(request, template_name)

class ParceiroCreate(CreateView):
    model = Parceiro
    template_name = 'blog/parceiro_form.html'
    form_class = ParceiroForm

class ParceiroUpdate(UpdateView):
    model = Parceiro
    template_name = 'blog/parceiro_form.html'
    form_class = ParceiroForm