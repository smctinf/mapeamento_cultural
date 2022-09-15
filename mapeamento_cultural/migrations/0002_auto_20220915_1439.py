# Generated by Django 3.2.15 on 2022-09-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapeamento_cultural', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area_atuacao',
            options={'ordering': ['area'], 'verbose_name': 'Área de Atuação', 'verbose_name_plural': 'Áreas de Atuação'},
        ),
        migrations.AlterModelOptions(
            name='enquadramento_atuacao',
            options={'ordering': ['enquadramento'], 'verbose_name': 'Enquadramento de atuação', 'verbose_name_plural': 'Enquadramentos de atuação'},
        ),
        migrations.AlterModelOptions(
            name='forma_insercao_atuacao',
            options={'ordering': ['forma'], 'verbose_name': 'Forma de inserção', 'verbose_name_plural': 'Formas de inserção'},
        ),
        migrations.AlterModelOptions(
            name='publico_atuacao',
            options={'ordering': ['publico'], 'verbose_name': 'Público', 'verbose_name_plural': 'Públicos'},
        ),
        migrations.AlterModelOptions(
            name='tiposcontratação',
            options={'ordering': ['nome'], 'verbose_name': 'Tipo de Contratação', 'verbose_name_plural': 'Tipos de Contratações'},
        ),
        migrations.AlterField(
            model_name='artista',
            name='banco',
            field=models.CharField(blank=True, choices=[('001', 'Banco do Brasil'), ('033', 'Banco Santander'), ('104', 'Caixa Econômica Federal'), ('237', 'Banco Bradesco'), ('341', 'Banco Itaú'), ('399', 'HSBC'), ('745', 'Banco Citibank'), ('260', 'Nu Bank'), ('out', 'Outro')], default='', max_length=3, null=True, verbose_name='Banco (Conta Corrente):'),
        ),
    ]
