# Generated by Django 2.2.12 on 2020-06-07 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_produto_tipo_produto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parceiro',
            name='parceiro_ativo',
        ),
    ]