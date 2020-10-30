from django.contrib import admin
from .models import Produto, EstoqueEntrada, EstoqueSaida, EstoqueItens, Parceiro

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'importado',
        'ncm',
        'preco',
        'estoque',
        'estoque_minimo', 
    )
    search_fields=('produto',)
    list_filter= ('importado',)

class EstoqueItensInline(admin.TabularInline):
    model = EstoqueItens
    extra = 0


@admin.register(EstoqueEntrada)
class EstoqueEntradaAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'nf','funcionario', )
    search_fields = ('nf',)
    list_filter = ('funcionario',)
    date_hierarchy = 'created'

@admin.register(EstoqueSaida)
class EstoqueSaidaAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'nf','funcionario', )
    search_fields = ('nf',)
    list_filter = ('funcionario',)
    date_hierarchy = 'created'
    

@admin.register(Parceiro)
class ParceiroAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'contato', 'telefone', 'estado', 'tipo_parceiro'
    )
    search_fields=('parceiro',)