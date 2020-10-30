# Generated by Django 2.2.12 on 2020-06-06 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_estoque_parceiro'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='tipo_produto',
            field=models.CharField(choices=[('Produto Acabado', 'Produto Acabado'), ('Matéria Prima', 'Matéria Prima')], default=2, max_length=30),
            preserve_default=False,
        ),
    ]