from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy


TIPOPARCEIRO = (
    ('Fornecedor', 'Fornecedor'),
    ('Cliente', 'Cliente'),
    ('Funcionário', 'Funcionário'),
    )
ESTADO = (
           ('AC', 'Acre'),
           ('AL', 'Alagoas'),
           ('AP', 'Amapá'),
           ('AM', 'Amazonas'),
           ('BA', 'Bahia'),
           ('CE', 'Ceará'),
           ('DF', 'Distrito Federal'),
           ('ES', 'Espírito Santo'),
           ('GO', 'Goiás'),
           ('MA', 'Maranhão'),
           ('MT', 'Mato Grosso'),
           ('MS', 'Mato Grosso do Sul'),
           ('MG', 'Minas Gerais'),
           ('PA', 'Pará'),
           ('PB', 'Paraíba'),
           ('PR', 'Paraná'),
           ('PE', 'Pernambuco'),
           ('PI', 'Piauí'),
           ('RJ', 'Rio de Janeiro'),
           ('RS', 'Rio Grande do Sul'),
           ('RO', 'Rondônia'),
           ('RR', 'Roraima'),
           ('SC', 'Santa Catarina'),
           ('SP', 'São Paulo'),
           ('SE', 'Sergipe'),
           ('TO', 'Tocantins'),
           )
class Parceiro (models.Model):
    parceiro = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)
    inscricao_estadual = models.CharField(max_length=50)
    contato = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)
    email = models.EmailField(max_length=300)
    rua = models.CharField(max_length=300)
    numero = models.CharField(max_length=9)
    cep = models.CharField(max_length=9)
    bairro = models.CharField(max_length=60)
    cidade = models.CharField(max_length=60)
    estado = models.CharField(max_length=15, choices=ESTADO)
    tipo_parceiro = models.CharField(max_length=50, choices=TIPOPARCEIRO)
    observacao = models.TextField()
    
    class meta:
        ordering= ('parceiro',)
    
    def __str__(self):
        return str(self.parceiro)

    def get_absolute_url(self):
        return reverse_lazy('blog:parceiro_detail', kwargs={'pk': self.pk})


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class TimeStampedModel (models.Model):
    created = models.DateTimeField(
         'Criado em ',
         auto_now_add=True,
         auto_now=False
    )
    modified = models.DateTimeField(
        'Modificado em',
        auto_now_add=False,
        auto_now=True
    )

    class Meta:
        abstract = True

TIPOPRODUTO = (
    ('Produto Acabado','Produto Acabado'),
    ('Matéria Prima','Matéria Prima'),
)
class Produto (models.Model):
    importado = models.BooleanField(default=False)
    ncm = models.CharField('NCM', max_length=8)
    produto = models.CharField(max_length=100)
    preco = models.DecimalField ('Preço', max_digits=7, decimal_places=2)
    estoque = models.IntegerField('estoque atual')
    estoque_minimo = models.PositiveIntegerField('Estoque Minímo', default=0)
    tipo_produto = models.CharField(max_length=30, choices=TIPOPRODUTO, blank=True)

    class meta:
        ordering= ('produto')

    def __str__(self):
        return str(self.produto)

    def get_absolute_url(self):
        return reverse_lazy('blog:detail_prod', kwargs={'pk': self.pk})
    
    def to_dict_json(self):
        return {
            'pk': self.pk,
            'produto': self.produto,
            'estoque': self.estoque,
        }

MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida'),
)

class Estoque (TimeStampedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    nf = models.PositiveIntegerField('nota fiscal', null=True, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO, blank=True)
    parceiro = models.ForeignKey(Parceiro, on_delete=models.CASCADE, )

    class meta:
        ordenring = ('-created') 

    def __str__(self):
        if self.nf:
            return '{} - {} - {}'.format(self.pk, self.nf, self.created.strftime('%d-%m-%Y'))
        return '{} --- {}'.format(self.pk,self.created.strftime('%d-%m-%Y'))

    def nf_formated(self):
        if self.nf:
            return str (self.nf).zfill(3)
        return '---'

class EstoqueEntradaManeger(models.Manager):
    def get_queryset(self):
        return super(EstoqueEntradaManeger, self).get_queryset().filter(movimento = 'e')

class EstoqueEntrada(Estoque):
    objects = EstoqueEntradaManeger()
    class Meta:
        proxy = True
        verbose_name = 'estoque entrada'
        verbose_name_plural = 'estoque entrada' 
    def get_absolute_url(self):
        return reverse_lazy('blog:ent_estoque_detail', kwargs={'pk': self.pk})

class EstoqueSaidaManeger(models.Manager):
    def get_queryset(self):
        return super(EstoqueSaidaManeger, self).get_queryset().filter(movimento = 's')

class EstoqueSaida(Estoque):
    objects = EstoqueSaidaManeger()
    class Meta:
        proxy = True
        verbose_name = 'estoque saida'
        verbose_name_plural = 'estoque saida' 
    
    def get_absolute_url(self):
        return reverse_lazy('blog:sai_estoque_detail', kwargs={'pk': self.pk})

class EstoqueItens(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='estoques')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    saldo = models.PositiveIntegerField(blank=True)

    class Meta:
        ordering=('pk',)

    def __str__(self):
        return '{} - {} - {}'.format (self.pk, self.estoque.pk, self.produto)

    
