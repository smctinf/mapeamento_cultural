# Generated by Django 3.2.13 on 2022-06-30 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtistaContratoCPF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(max_length=11, verbose_name='CPF do proponente:')),
                ('file_cpf', models.FileField(upload_to='file_cpf', verbose_name='CPF - Documento scaneado:')),
                ('file_comprovante_residencia', models.FileField(upload_to='file_comprovantes_residencia', verbose_name='Comprovante de residência - Documento scaneado:')),
                ('pis', models.CharField(max_length=80, verbose_name='PIS/PASEP/NIT')),
                ('file_pis', models.FileField(upload_to='file_pis', verbose_name='PIS/PASEP/NIT - Documento scaneado:')),
                ('banco', models.CharField(default='', max_length=80, verbose_name='Banco (Conta Corrente):')),
                ('agencia', models.CharField(default='', max_length=80, verbose_name='Agência:')),
                ('n_conta', models.CharField(default='', max_length=80, verbose_name='Número da conta')),
                ('comprovante_de_cc', models.FileField(upload_to='file_comprovante_cc', verbose_name='Comprovante de número de conta corrente (banco, agência e nº da conta):')),
                ('declaracao_n_viculo', models.FileField(upload_to='file_declaracao_n_vinculo', verbose_name='Declaração de não vínculo com a Administração Federal, Estadual e Municipal:')),
                ('comprovante_iss', models.FileField(upload_to='file_comprovante_iss', verbose_name='Comprovante de inscrição do ISS Municipal:')),
                ('comprovante_recibos', models.FileField(upload_to='file_comprovante_recibos', verbose_name='Recibos, contratos ou notas que comprovem cachê:')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')),
            ],
        ),
        migrations.CreateModel(
            name='TiposContratação',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ArtistaContratoCNPJ',
            fields=[
                ('artistacontratocpf_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mapeamento_cultural.artistacontratocpf')),
                ('cnpj', models.CharField(max_length=11, verbose_name='CNPJ do proponente:')),
                ('file_cnpj', models.FileField(upload_to='file_cnpj', verbose_name='CNPJ - Documento scaneado evidenciando cadastro em atividades da àrea cultural:')),
                ('prova_inscricao_PJ_nacional', models.FileField(upload_to='prova_inscricao_PJ_nacional', verbose_name='Prova de inscrição no Cadastro Nacional de Pessoa Jurídica:')),
                ('certidao_negativa_debitos_relativos', models.FileField(upload_to='certidao_negativa_debitos_relativos', verbose_name='Certidão Negativa de Débitos Relativos a TRibunais Federais e à Divida Ativa da União:')),
                ('certidao_regularidade_icms', models.FileField(upload_to='certidao_regularidade_icms', verbose_name='Certidão de Regularidade de Tribunais Estaduais (ICMS):')),
                ('certidao_regularidade_iss', models.FileField(upload_to='certidao_regularidade_iss', verbose_name='Certidão de Regularidade de Tribunais Municipais (ISS):')),
                ('certidao_negativa_debitos', models.FileField(upload_to='certidao_negativa_debitos', verbose_name='Certidão Negativa de Débitos:')),
                ('certidao_regularidade_situacao', models.FileField(upload_to='certidao_de_regularidade_de_situacao', verbose_name='Certidão de REgularidade de Situação:')),
                ('certidao_negativa_debitos_trabalhistas', models.FileField(upload_to='certidao_debitos_trabalhistas_cndt', verbose_name='Certidão de Negativa de Débitos Trabalhistas - CDNT:')),
            ],
            bases=('mapeamento_cultural.artistacontratocpf',),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rg', models.CharField(max_length=40, verbose_name='RG:')),
                ('cpf', models.CharField(max_length=11, verbose_name='CPF:')),
                ('email', models.EmailField(max_length=254, verbose_name='Email:')),
                ('endereco', models.CharField(max_length=40, verbose_name='Endereço:')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='artistacontratocpf',
            name='tipo_contratacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mapeamento_cultural.tiposcontratação', verbose_name='Tipo de contratação:'),
        ),
        migrations.AddField(
            model_name='artistacontratocpf',
            name='user_responsavel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
