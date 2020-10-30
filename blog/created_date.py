import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projetoec2.settings")
django.setup()

import string
import timeit
from random import choice, random, randint
from projetoec2.produto.models import Produto

class utils:
    @staticmethod
    def gen_digits(max_length):
        return str(''.join(choice(string.digits)for i in range(max_length)))

class ProdutoClass:
    @staticmethod
    def criar_produtos (produtos):
        Produto.objects.all().delete()
        aux = []
        for produto in produtos:
            data = dict(
                produto = produto,
                importado = choice((True, False)),
                ncm = utils.gen_digits(8),
                preco = random() * randint(10,50),
                estoque = randint(10,200),
            )
            obj = Produto(**data)
            aux.append(obj)
        Produto.objects.bulk_create(aux)

produtos = (
    'Produto A',
    'Produto B',
    'Produto C',
    'Produto D',
)

tic = timeit.default_timer()

ProdutoClass.criar_produtos(produtos)

toc = timeit.default_timer()

print('Tempo:' , toc, tic)

