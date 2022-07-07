from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)    
    rg=models.CharField(max_length=40, verbose_name='RG:')
    cpf=models.CharField(max_length=11, verbose_name='CPF:')
    email=models.EmailField(verbose_name='Email:')
    endereco=models.CharField(max_length=40, verbose_name='Endereço:')
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')

class TiposContratação(models.Model):

    nome=models.CharField(max_length=50)

    def __str__(self):
        return '%s' % (self.nome)

# class Artista(models.Model):
#     nome_artistico=models.CharField(max_length=300)
#     data_de_registro=models.DateField()
#     telefone_contato=models.CharField(max_length=11)
#     endereco=models.CharField(max_length=350)
    
class ArtistaContratoCPF(models.Model):
    
    fazedor_cultura=models.CharField(max_length=100, verbose_name='Nome artístico do Fazedor de Cultura:')
    descricao=models.TextField(verbose_name='Descrição resumida da atividade artística/culturais desenvolvidas:')
    tipo_contratacao=models.ForeignKey(TiposContratação, verbose_name='Tipo de contratação:', on_delete=models.PROTECT, blank=True, null=True)    
    cpf=models.CharField(max_length=11, verbose_name='CPF do proponente:')
    file_cpf=models.FileField(upload_to='file_cpf', verbose_name='CPF - Documento scaneado:')   
    file_comprovante_residencia=models.FileField(upload_to='file_comprovantes_residencia', verbose_name='Comprovante de residência - Documento scaneado:')
    pis=models.CharField(max_length=80, verbose_name='PIS/PASEP/NIT')
    file_pis=models.FileField(upload_to='file_pis', verbose_name='PIS/PASEP/NIT - Documento scaneado:')
    banco=models.CharField(max_length=80, verbose_name='Banco (Conta Corrente):', default='')
    agencia=models.CharField(max_length=80, verbose_name='Agência:', default='')
    n_conta=models.CharField(max_length=80, verbose_name='Número da conta', default='')
    comprovante_de_cc=models.FileField(upload_to='file_comprovante_cc', verbose_name='Comprovante de número de conta corrente (banco, agência e nº da conta):')
    declaracao_n_viculo=models.FileField(upload_to='file_declaracao_n_vinculo', verbose_name='Declaração de não vínculo com a Administração Federal, Estadual e Municipal:')    
    comprovante_iss=models.FileField(upload_to='file_comprovante_iss', verbose_name='Comprovante de inscrição do ISS Municipal:')
    comprovante_recibos=models.FileField(upload_to='file_comprovante_recibos', verbose_name='Recibos, contratos ou notas que comprovem cachê:')
    user_responsavel=models.ForeignKey(User, on_delete=models.CASCADE, null=True)    
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')

class ArtistaContratoCNPJ(ArtistaContratoCPF):

    cnpj=models.CharField(max_length=11, verbose_name='CNPJ do proponente:')    
    file_cnpj=models.FileField(upload_to='file_cnpj', verbose_name='CNPJ - Documento scaneado evidenciando cadastro em atividades da àrea cultural:')
    prova_inscricao_PJ_nacional=models.FileField(upload_to='prova_inscricao_PJ_nacional', verbose_name='Prova de inscrição no Cadastro Nacional de Pessoa Jurídica:')
    certidao_negativa_debitos_relativos=models.FileField(upload_to='certidao_negativa_debitos_relativos', verbose_name='Certidão Negativa de Débitos Relativos a TRibunais Federais e à Divida Ativa da União:')
    certidao_regularidade_icms=models.FileField(upload_to='certidao_regularidade_icms', verbose_name='Certidão de Regularidade de Tribunais Estaduais (ICMS):')
    certidao_regularidade_iss=models.FileField(upload_to='certidao_regularidade_iss', verbose_name='Certidão de Regularidade de Tribunais Municipais (ISS):')
    certidao_negativa_debitos=models.FileField(upload_to='certidao_negativa_debitos', verbose_name='Certidão Negativa de Débitos:')
    certidao_regularidade_situacao=models.FileField(upload_to='certidao_de_regularidade_de_situacao', verbose_name='Certidão de REgularidade de Situação:')
    certidao_negativa_debitos_trabalhistas=models.FileField(upload_to='certidao_debitos_trabalhistas_cndt', verbose_name='Certidão de Negativa de Débitos Trabalhistas - CDNT:')

class ArtistaContratoEmpresario(ArtistaContratoCNPJ):

    documento_empresario_exclusivo=models.FileField(upload_to='documento_empresario_exclusivo', verbose_name="Documento que comprove que o prestador é exclusivo do 'fazedor de cultura' em questão.*:")    


class Area_Atuacao(models.Model):
    
    area=models.CharField(max_length=150)
    def __str__(self):
        return '%s' % (self.area)

class Publico_Atuacao(models.Model):
    
    publico=models.CharField(max_length=150)
    def __str__(self):
        return '%s' % (self.publico)

class Enquadramento_Atuacao(models.Model):    

    enquadramento=models.CharField(max_length=150)
    def __str__(self):
        return '%s' % (self.enquadramento)


class Forma_insercao_Atuacao(models.Model):
    
    forma=models.CharField(max_length=150)
    def __str__(self):
        return '%s' % (self.forma)



class InformacoesExtras(models.Model):
    
    STATUS_CHOICES=[
        ('p', 'Principal (maior fonte de renda/profissão)'),
        ('s', 'secundaria (renda extra, ou prática sem fins lucrativos como lazer)')
    ]

    QNT_CHOICES=[
        ('0', '0 a 10'),
        ('1', '11 a 20'),
        ('2', '21 a 30'),
        ('3', '31 a 40'),
        ('4', '41 a 50'),
        ('5', 'Mais de 50'),
    ]
    
    TIPO_CHOICES=[
        ('cpf', 'CPF'),
        ('cnpj', 'CNPJ'),                
    ]    

    tipo=models.CharField(max_length=6, choices=TIPO_CHOICES)
    id_artista=models.CharField(max_length=20)
    area=models.ManyToManyField(Area_Atuacao)
    publico=models.ManyToManyField(Publico_Atuacao)
    enquadramento=models.ManyToManyField(Enquadramento_Atuacao)
    forma_atuacao=models.ManyToManyField(Forma_insercao_Atuacao)
    qnt=models.CharField(max_length=1, choices=QNT_CHOICES)
    status=models.CharField(max_length=1, choices=STATUS_CHOICES)
    instagram=models.CharField(max_length=150, blank=True)
    facebook=models.CharField(max_length=150, blank=True)
    youtube=models.CharField(max_length=150, blank=True)