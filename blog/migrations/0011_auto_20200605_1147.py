# Generated by Django 2.2.12 on 2020-06-05 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200605_1029'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parceiro',
            old_name='CEP',
            new_name='cep',
        ),
        migrations.RenameField(
            model_name='parceiro',
            old_name='Cidade',
            new_name='cidade',
        ),
        migrations.RenameField(
            model_name='parceiro',
            old_name='Cnpj',
            new_name='cnpj',
        ),
        migrations.RenameField(
            model_name='parceiro',
            old_name='Email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='parceiro',
            old_name='Estado',
            new_name='estado',
        ),
        migrations.RenameField(
            model_name='parceiro',
            old_name='Inscricao_estadual',
            new_name='inscricao_estadual',
        ),
        migrations.RenameField(
            model_name='parceiro',
            old_name='Observacao',
            new_name='observacao',
        ),
        migrations.RenameField(
            model_name='parceiro',
            old_name='Telefone_1',
            new_name='telefone',
        ),
    ]