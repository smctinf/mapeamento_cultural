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
    
class ArtistaContrato(models.Model):

    tipo_contratacao=models.ForeignKey(TiposContratação, verbose_name='Tipo de contratação:', on_delete=models.PROTECT, blank=True, null=True)    
    cpf=models.CharField(max_length=11, verbose_name='CPF do artista:')
    file_cpf=models.FileField(upload_to='file_cpf', verbose_name='CPF - Documento scaneado:')
    file_comprovante_residencia=models.FileField(upload_to='file_comprovantes_residencia', verbose_name='Comprovante de residência - Documento scaneado:')
    pis=models.CharField(max_length=80, verbose_name='PIS/PASEP/NIT')
    file_pis=models.FileField(upload_to='file_pis', verbose_name='PIS - Documento scaneado:')
    banco=models.CharField(max_length=80, verbose_name='Banco (Conta Corrente):')
    agencia=models.CharField(max_length=80, verbose_name='Agência:')
    n_conta=models.CharField(max_length=80, verbose_name='Número da conta')
    declaracao_n_viculo=models.FileField(upload_to='file_declaracao_n_vinculo', verbose_name='Declaração de não vínculo com a Administração Federal, Estadual e Municipal:')
    comprovante_iss=models.FileField(upload_to='file_comprovante_iss', verbose_name='Comprovante de inscrição do ISS Municipal:')
    comprovante_recibos=models.FileField(upload_to='file_comprovante_recibos', verbose_name='Recibos, contratos ou notas que comprovem cachê:')
    user_responsavel=models.ForeignKey(User, on_delete=models.CASCADE, null=True)    
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')


