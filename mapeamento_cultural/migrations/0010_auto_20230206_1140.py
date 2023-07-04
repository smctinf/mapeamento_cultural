# Generated by Django 3.2.16 on 2023-02-06 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapeamento_cultural', '0009_alter_artista_prova_inscricao_pj_nacional_validade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artista',
            name='area',
            field=models.ManyToManyField(to='mapeamento_cultural.Area_Atuacao', verbose_name='Área(s) de atuação'),
        ),
        migrations.AlterField(
            model_name='informacoesextras',
            name='enquadramento',
            field=models.ManyToManyField(to='mapeamento_cultural.Enquadramento_Atuacao', verbose_name='Enquadramento da instituição/entidade/coletivo/grupo'),
        ),
        migrations.AlterField(
            model_name='informacoesextras',
            name='forma_atuacao',
            field=models.ManyToManyField(to='mapeamento_cultural.Forma_insercao_Atuacao', verbose_name='Forma de inserção da atividade artístico-cultural'),
        ),
        migrations.AlterField(
            model_name='informacoesextras',
            name='publico',
            field=models.ManyToManyField(to='mapeamento_cultural.Publico_Atuacao', verbose_name='Públicos que participam das ações'),
        ),
    ]