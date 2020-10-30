from django import forms
from .models import Produto, Estoque, EstoqueItens, Parceiro

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'

class ParceiroForm(forms.ModelForm):
    class Meta:
        model = Parceiro
        fields = '__all__'

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ('nf','parceiro',)

class EstoqueItensForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = '__all__'

class EstoqueItensSaidaForm(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EstoqueItensSaidaForm, self).__init__(*args, **kwargs)
        # Retorna somente produtos com estoque maior do que zero.
        self.fields['produto'].queryset = Produto.objects.filter(estoque__gt=0)
