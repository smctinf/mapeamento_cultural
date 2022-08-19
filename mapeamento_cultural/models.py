from ast import Delete
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from .validations import *
import os
from cultura.settings import BASE_DIR   
class Usuario(models.Model):
    
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)    
    # rg=models.CharField(max_length=40, verbose_name='RG:')
    cpf=models.CharField(max_length=14, verbose_name='CPF:', validators=[validate_CPF], unique=True)
    data_nascimento = models.DateField(verbose_name='Data Nascimento')
    email=models.EmailField(verbose_name='Email:', unique=True)
    endereco=models.CharField(max_length=40, verbose_name='Endereço:')
    bairro=models.CharField(max_length=40, verbose_name='Bairro:')
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')

    __original_email = None
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.user is not None:
            if self.email != self.__original_email:
                self.user.username = self.email
                self.user.email = self.email
                self.user.save()

        super().save(force_insert, force_update, *args, **kwargs)
        self.__original_email = self.email

class TiposContratação(models.Model):

    nome=models.CharField(max_length=50)

    def __str__(self):
        return '%s' % (self.nome)

# class Artista(models.Model):
#     nome_artistico=models.CharField(max_length=300)
#     data_de_registro=models.DateField()
#     telefone_contato=models.CharField(max_length=11)
#     endereco=models.CharField(max_length=350)

class Area_Atuacao(models.Model):
    
    area=models.CharField(max_length=150)
    
    def __str__(self):
        return '%s' % (self.area)
    
    class Meta:
        ordering = ["area"]
   
class Publico_Atuacao(models.Model):
    
    publico=models.CharField(max_length=150)
    def __str__(self):
        return '%s' % (self.publico)
    
    class Meta:
        ordering = ["publico"]
        
class Enquadramento_Atuacao(models.Model):    

    enquadramento=models.CharField(max_length=150)
    def __str__(self):
        return '%s' % (self.enquadramento)

    class Meta:
        ordering = ["enquadramento"]

class Forma_insercao_Atuacao(models.Model):
    
    forma=models.CharField(max_length=150)
    def __str__(self):
        return '%s' % (self.forma)

    class Meta:
        ordering = ["forma"]


class InformacoesExtras(models.Model):
    
    STATUS_CHOICES=[
        ('p', 'Principal (maior fonte de renda/profissão)'),
        ('s', 'Secundaria (renda extra, ou prática sem fins lucrativos como lazer)')
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
        ('1', 'CPF'),
        ('2', 'CNPJ'),                
    ]    
    
    id_artista=models.CharField(max_length=20, blank=True)    
    descricao=models.TextField(verbose_name='Descrição resumida da atividade artística/culturais desenvolvidas', blank=True, null=True)    
    publico=models.ManyToManyField(Publico_Atuacao, blank=True, verbose_name='Públicos que participam das ações')
    enquadramento=models.ManyToManyField(Enquadramento_Atuacao, blank=True, verbose_name='Enquadramento da instituição/entidade/coletivo/grupo')
    forma_atuacao=models.ManyToManyField(Forma_insercao_Atuacao, blank=True, verbose_name='Formar de inserção da atividade artístico-cultural')
    endereco=models.CharField(max_length=150, blank=True, verbose_name='Endereço')
    qnt=models.CharField(max_length=1, choices=QNT_CHOICES, blank=True, null=True, verbose_name='Quantidade de pessoas que fazem parte da instituição')
    status=models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, verbose_name='Status da atividade')
    instagram=models.CharField(max_length=150, blank=True)
    facebook=models.CharField(max_length=150, blank=True)
    youtube=models.CharField(max_length=150, blank=True)
    complete=models.BooleanField(default=False)


class Artista(models.Model):
    
    fazedor_cultura=models.CharField(max_length=100, verbose_name='Nome artístico', blank=True, null=True)    
    area=models.ManyToManyField(Area_Atuacao, verbose_name='Área(s) de atuação', blank=True, null=True)
    
    # email=models.EmailField()
    telefone=models.CharField(max_length=15, validators=[validate_TELEFONE])    
    tipo_contratacao=models.ForeignKey(TiposContratação, verbose_name='Tipo de contratação', on_delete=models.PROTECT, blank=True, null=True)        
    file_cpf=models.FileField(upload_to='file_cpf', verbose_name='CPF', blank=True, null=True)   
    file_comprovante_residencia=models.FileField(upload_to='file_comprovantes_residencia', verbose_name='Comprovante de residência', blank=True, null=True)
    pis=models.CharField(max_length=80, verbose_name='PIS/PASEP/NIT', blank=True, null=True)
    file_pis=models.FileField(upload_to='file_pis', verbose_name='PIS/PASEP/NIT', blank=True, null=True)
    banco=models.CharField(verbose_name='Banco (Conta Corrente):', default='', max_length=3, blank=True, null=True)
    agencia=models.CharField(verbose_name='Agência:', default='', max_length=4, blank=True, null=True)
    n_conta=models.CharField(verbose_name='Número da conta', default='', max_length=8, blank=True, null=True)
    comprovante_de_cc=models.FileField(upload_to='file_comprovante_cc', verbose_name='Comprovante de número de conta corrente (banco, agência e nº da conta)', blank=True, null=True)
    declaracao_n_viculo=models.FileField(upload_to='file_declaracao_n_vinculo', verbose_name='Declaração de não vínculo com a Administração Federal, Estadual e Municipal', blank=True, null=True)    
    comprovante_iss=models.FileField(upload_to='file_comprovante_iss', verbose_name='Comprovante de inscrição do ISS Municipal', blank=True, null=True)
    
    cadastro_completo=models.BooleanField(default=False)
    fazedor_cultura_cnpj=models.CharField(max_length=100, verbose_name='Nome fantasia', blank=True, null=True)
    cnpj=models.CharField(max_length=18, verbose_name='CNPJ', validators=[validate_CNPJ], null=True, unique=True)  
    # cpf_responsavel=models.CharField(max_length=14, verbose_name='CPF do responsável', validators=[validate_CPF], blank=True, null=True)
    file_cnpj=models.FileField(upload_to='file_cnpj', verbose_name='CNPJ - Documento scaneado evidenciando cadastro em atividades da àrea cultural', blank=True, null=True)
    prova_inscricao_PJ_nacional=models.FileField(upload_to='prova_inscricao_PJ_nacional', verbose_name='Prova de inscrição no Cadastro Nacional de Pessoa Jurídica', blank=True, null=True)
    certidao_negativa_debitos_relativos=models.FileField(upload_to='certidao_negativa_debitos_relativos', verbose_name='Certidão Negativa de Débitos Relativos a Tribunais Federais e à Divida Ativa da União', blank=True, null=True)
    certidao_regularidade_icms=models.FileField(upload_to='certidao_regularidade_icms', verbose_name='Certidão de Regularidade de Tribunais Estaduais (ICMS)', blank=True, null=True)
    certidao_regularidade_iss=models.FileField(upload_to='certidao_regularidade_iss', verbose_name='Certidão de Regularidade de Tribunais Municipais (ISS)', blank=True, null=True)
    certidao_negativa_debitos=models.FileField(upload_to='certidao_negativa_debitos', verbose_name='Certidão Negativa de Débitos', blank=True, null=True)
    certidao_regularidade_situacao=models.FileField(upload_to='certidao_de_regularidade_de_situacao', verbose_name='Certidão de REgularidade de Situação', blank=True, null=True)
    certidao_negativa_debitos_trabalhistas=models.FileField(upload_to='certidao_debitos_trabalhistas_cndt', verbose_name='Certidão de Negativa de Débitos Trabalhistas - CDNT', blank=True, null=True)
    documento_empresario_exclusivo=models.FileField(upload_to='documento_empresario_exclusivo', verbose_name="Documento que comprove que o prestador é exclusivo do 'fazedor de cultura' em questão.*", blank=True, null=True)    
    user_responsavel=models.ForeignKey(User, on_delete=models.CASCADE, null=True)        
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')

    def delete(self):
        #deletar anexos
        anexos = [
            self.file_cpf,
            self.prova_inscricao_PJ_nacional,
            self.file_comprovante_residencia,
            self.file_pis,
            self.comprovante_de_cc,
            self.declaracao_n_viculo,
            self.comprovante_iss,
            self.certidao_negativa_debitos_relativos,
            self.certidao_regularidade_icms,
            self.certidao_regularidade_iss,
            self.certidao_negativa_debitos,
            self.certidao_regularidade_situacao,
            self.certidao_negativa_debitos_trabalhistas,
            self.documento_empresario_exclusivo
        ]
        
        for i in anexos:
            if i != '':
                try:
                    url_path=str(BASE_DIR)+'/cultura/media/'+str(i)
                    os.remove(url_path)
                except Exception as e:
                    print(e)
        #deletar informações extras
        try:
            info=InformacoesExtras.objects.get(id_artista=self.id)
            info.delete()
        except Exception as e:
            print(e)

        super(Artista, self).delete()

class Recibos(models.Model):
    comprovante=models.FileField(upload_to='file_comprovante_recibos', verbose_name='Recibos, contratos ou notas que comprovem cachê', blank=True, null=True)
    artista=models.ForeignKey(Artista, on_delete=models.CASCADE, verbose_name='Artista', blank=True, null=True)

    def delete(self):            
            if self.comprovante != '':                
                try:
                    url_path=str(BASE_DIR)+'/cultura/media/'+str(self.comprovante)
                    os.remove(url_path)
                except Exception as e:
                    print(e)
            super(Recibos, self).delete()


class Log_anexos(models.Model):
    artista=models.ForeignKey(Artista, on_delete=models.CASCADE, verbose_name='Artista')
    anexo=models.CharField(max_length=150, verbose_name='Anexo')
    filename=models.CharField(max_length=150, verbose_name='Nome do arquivo')
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')
    dt_alteration = models.DateTimeField(auto_now=True, verbose_name='Dt. Alteração')
    user_responsavel=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
