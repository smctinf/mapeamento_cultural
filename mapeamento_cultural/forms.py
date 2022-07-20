from django import forms
from django.forms import ModelForm, ValidationError
from .models import *

class Form_Usuario(ModelForm):  
    
    class Meta:
        model = Usuario
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder':''}),
            # 'rg': forms.TextInput(attrs={'placeholder':''}),            
            'cpf': forms.TextInput(attrs={'placeholder':'', 'onkeydown':'mascara(this,icpf)'}),
            'endereco': forms.TextInput(attrs={'placeholder':''}),
        }        
        exclude = ['dt_inclusao', 'user']
    
    def clean_cpf(self):
        cpf = validate_CPF(self.cleaned_data["cpf"])
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
        return cpf


class Form_Artista(ModelForm):

    class Meta:
        model = Artista
        widgets = {
            # 'nome_artistico': forms.EmailInput(attrs={'placeholder':''}),
            'cpf': forms.TextInput(attrs={'onkeydown': 'mascara(this,icpf)'}),                        
            
            'descricao': forms.TextInput(attrs={'placeholder':''}),                        
            'pis': forms.TextInput(attrs={'placeholder':''}),                        
            'banco': forms.TextInput(attrs={'placeholder':'', 'onkeydown': 'mascara(this,apenasNumeros)'}),                      
            'agencia': forms.TextInput(attrs={'placeholder':'', 'onkeydown': 'mascara(this,apenasNumeros)'}),                        
            'n_conta': forms.TextInput(attrs={'placeholder':'', 'onkeydown': 'mascara(this,apenasNumeros)'}),                        
        }        
        fields=['fazedor_cultura', 'cpf', 'data_nascimento', 'area', 'email', 'telefone']

    field_order=['fazedor_cultura', 'cpf', 'data_nascimento', 'area', 'email', 'telefone']

    def clean_cpf(self):
        cpf = validate_CPF(self.cleaned_data["cpf"])
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
        return cpf

class Form_Artista2(ModelForm):

    class Meta:        
        model = Artista
        widgets = {
            # 'nome_artistico': forms.EmailInput(attrs={'placeholder':''}),
            'descricao': forms.Textarea(attrs={'placeholder':'', 'rows':'3'}),
            'pis': forms.TextInput(attrs={'placeholder':'',}),                  
            'banco': forms.TextInput(attrs={'placeholder':'',}),
            'agencia': forms.TextInput(attrs={'placeholder':'',}),
            'n_conta': forms.TextInput(attrs={'placeholder':'',}),
        }        
        fields = [
            'descricao',           
            'pis',            
            'banco',
            'agencia',
            'n_conta',             
            ]               
    
    field_order=['fazedor_cultura', 'cpf', 'data_nascimento', 'area', 'email', 'telefone']

    def clean_cpf(self):
        cpf = validate_CPF(self.cleaned_data["cpf"])
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
        return cpf

class Form_Anexo_Artista_CPF(ModelForm):

    class Meta:
        model = Artista
        fields = [
            'file_cpf',
            'file_comprovante_residencia',
            'file_pis',
            'comprovante_de_cc',
            'declaracao_n_viculo',
            'comprovante_iss',
            'comprovante_iss',
            'comprovante_recibos',
        ]

class Form_Anexo_Artista_CNPJ(ModelForm):

    class Meta:
        model = Artista
        fields = [
            'prova_inscricao_PJ_nacional',
            'file_comprovante_residencia',
            'file_pis',
            'comprovante_de_cc',
            'declaracao_n_viculo',
            'comprovante_iss',
            'comprovante_iss',
            'comprovante_recibos',
            'certidao_negativa_debitos_relativos',
            'certidao_regularidade_icms',
            'certidao_regularidade_iss',
            'certidao_negativa_debitos',
            'certidao_regularidade_situacao',
             'certidao_negativa_debitos_trabalhistas',
             'documento_empresario_exclusivo'
        ]
class Form_ArtistaCNPJ(ModelForm):
    class Meta:
        model = Artista
        widgets = {
            # 'nome_artistico': forms.EmailInput(attrs={'placeholder':''}),
            'cnpj': forms.TextInput(attrs={'onkeydown': 'mascara(this,icnpj)'}), 
            'cpf_responsavel': forms.TextInput(attrs={'onkeydown': 'mascara(this,icpf)'}),                        
            'fazedor_cultura': forms.TextInput(attrs={'placeholder':''}),                        
            'descricao': forms.TextInput(attrs={'placeholder':''}),                        
            'pis': forms.TextInput(attrs={'placeholder':''}),                        
            'banco': forms.TextInput(attrs={'placeholder':'', 'onkeydown': 'mascara(this,apenasNumeros)'}),                      
            'agencia': forms.TextInput(attrs={'placeholder':'', 'onkeydown': 'mascara(this,apenasNumeros)'}),                        
            'n_conta': forms.TextInput(attrs={'placeholder':'', 'onkeydown': 'mascara(this,apenasNumeros)'}),                           
        }        
        exclude = [
            'fazedor_cultura',
            'data_nascimento',
            'descricao',
            'cpf',
            'file_cpf',
            'file_comprovante_residencia',
            'pis',
            'file_pis',
            'banco',
            'agencia',
            'n_conta',
            'comprovante_de_cc',
            'declaracao_n_viculo',
            'comprovante_iss',
            'comprovante_iss',
            'comprovante_recibos',
            'file_cnpj',
            'prova_inscricao_PJ_nacional',
            'certidao_negativa_debitos_relativos',
            'certidao_regularidade_icms',
            'certidao_regularidade_iss',
            'certidao_regularidade_iss',
            'certidao_negativa_debitos',
            'certidao_regularidade_situacao',
            'certidao_negativa_debitos_trabalhistas',
            'documento_empresario_exclusivo',
            'tipo_contratacao',
            'cadastro_completo',
            'dt_inclusao',
            'user_responsavel']
    field_order=['fazedor_cultura_cnpj', 'cnpj', 'area', 'data_nascimento', 'email', 'telefone', 'cpf_responsavel']
    
    def clean_cnpj(self):
        cnpj = validate_CNPJ(self.cleaned_data["cnpj"])
        cnpj = cnpj.replace('.', '')
        cnpj = cnpj.replace('/', '')
        cnpj = cnpj.replace('-', '')
        return cnpj


    def clean_cpf_responsavel(self):
        cpf = validate_CPF(self.cleaned_data["cpf_responsavel"])
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
        return cpf
class Form_ArtistaEmpresa(ModelForm):
    class Meta:
        model = Artista
        widgets = {
            # 'nome_artistico': forms.EmailInput(attrs={'placeholder':''}),
            'cnpj': forms.TextInput(attrs={'placeholder':''}),   
            'cpf': forms.TextInput(attrs={'placeholder':'', 'onkeydown': 'mascara(this,icpf)'}),                        
            'fazedor_cultura': forms.TextInput(attrs={'placeholder':''}),                        
            'descricao': forms.TextInput(attrs={'placeholder':''}),                        
            'pis': forms.TextInput(attrs={'placeholder':''}),                        
            'banco': forms.TextInput(attrs={'placeholder':'', 'onkeydown': 'mascara(this,apenasNumeros)'}),                      
            'agencia': forms.TextInput(attrs={'placeholder':'', 'onkeydown': 'mascara(this,apenasNumeros)'}),                        
            'n_conta': forms.TextInput(attrs={'placeholder':'', 'onkeydown': 'mascara(this,apenasNumeros)'}),                         
        }        
        exclude = [
            'fazedor_cultura',
            'cpf',
            'data_nascimento',
            'descricao',
            'file_cpf',
            'file_comprovante_residencia',
            'pis',
            'file_pis',
            'banco',
            'agencia',
            'n_conta',
            'comprovante_de_cc',
            'declaracao_n_viculo',
            'comprovante_iss',
            'comprovante_iss',
            'comprovante_recibos',            
            'file_cnpj',
            'prova_inscricao_PJ_nacional',
            'certidao_negativa_debitos_relativos',
            'certidao_regularidade_icms',
            'certidao_regularidade_iss',
            'certidao_regularidade_iss',
            'certidao_negativa_debitos',
            'certidao_regularidade_situacao',
            'certidao_negativa_debitos_trabalhistas',
            'documento_empresario_exclusivo',
            'tipo_contratacao',
            'dt_inclusao',
            'user_responsavel']

    field_order=['fazedor_cultura_cnpj', 'cnpj', 'area', 'data_nascimento', 'email', 'telefone', 'cpf_responsavel']

class Form_InfoExtra(ModelForm):
    class Meta:
        model = InformacoesExtras
        widgets = {
            'tipo': forms.HiddenInput(),
            'id_artista': forms.HiddenInput(attrs={'class': 'mb-3'}),            
            'area': forms.CheckboxSelectMultiple(attrs={'class': 'mb-3'}),
            'publico': forms.CheckboxSelectMultiple(attrs={'class': 'mb-3'}),
            'enquadramento': forms.CheckboxSelectMultiple(attrs={'class': 'mb-3'}),
            'forma_atuacao': forms.CheckboxSelectMultiple(attrs={'class': 'mb-3'}),
            'endereco': forms.TextInput(attrs={'placeholder':'', 'class': 'form-control mb-3'}),
            'qnt': forms.Select(attrs={'class': 'form-control mb-3'}),
            'status': forms.Select(attrs={'class': 'form-control mb-3'}),
            'instagram': forms.TextInput(attrs={'placeholder':'', 'class': 'form-control mb-3'}),
            'facebook': forms.TextInput(attrs={'placeholder':'', 'class': 'form-control mb-3'}),
            'youtube': forms.TextInput(attrs={'placeholder':'', 'class': 'form-control mb-3'}),
        }        
        exclude = ['complete']