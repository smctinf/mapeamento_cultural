from django import forms
from django.forms import ModelForm, ValidationError
from .models import *

class Form_Usuario(ModelForm):  
    
    class Meta:
        model = Usuario
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder':''}),
            'rg': forms.TextInput(attrs={'placeholder':''}),            
            'cpf': forms.TextInput(attrs={'placeholder':''}),
            'endereco': forms.TextInput(attrs={'placeholder':''}),
        }        
        exclude = ['dt_inclusao', 'user']

    # def clean_cnpj(self):
    #     print(self.cleaned_data["cnpj"])
    #     cnpj = validate_CNPJ(self.cleaned_data["cnpj"])
    #     cnpj = cnpj.replace('.', '')
    #     cnpj = cnpj.replace('-', '')
    #     return cnpj

class Form_Artista(ModelForm):
    class Meta:
        model = ArtistaContratoCPF
        widgets = {
            # 'nome_artistico': forms.EmailInput(attrs={'placeholder':''}),
            'cpf': forms.TextInput(attrs={'placeholder':''}),                        
            'fazedor_cultura': forms.TextInput(attrs={'placeholder':''}),                        
            'descricao': forms.TextInput(attrs={'placeholder':''}),                        
            'pis': forms.TextInput(attrs={'placeholder':''}),                        
            'banco': forms.TextInput(attrs={'placeholder':''}),                      
            'agencia': forms.TextInput(attrs={'placeholder':''}),                        
            'n_conta': forms.TextInput(attrs={'placeholder':''}),                        
        }        
        exclude = ['cnpj', 'tipo_contratacao', 'dt_inclusao', 'user_responsavel']

class Form_ArtistaCNPJ(ModelForm):
    class Meta:
        model = ArtistaContratoCNPJ
        widgets = {
            # 'nome_artistico': forms.EmailInput(attrs={'placeholder':''}),
            'cnpj': forms.TextInput(attrs={'placeholder':''}), 
            'cpf': forms.TextInput(attrs={'placeholder':''}),                        
            'fazedor_cultura': forms.TextInput(attrs={'placeholder':''}),                        
            'descricao': forms.TextInput(attrs={'placeholder':''}),                        
            'pis': forms.TextInput(attrs={'placeholder':''}),                        
            'banco': forms.TextInput(attrs={'placeholder':''}),                      
            'agencia': forms.TextInput(attrs={'placeholder':''}),                        
            'n_conta': forms.TextInput(attrs={'placeholder':''}),                           
        }        
        exclude = ['tipo_contratacao', 'dt_inclusao', 'user_responsavel']

class Form_ArtistaEmpresa(ModelForm):
    class Meta:
        model = ArtistaContratoEmpresario
        widgets = {
            # 'nome_artistico': forms.EmailInput(attrs={'placeholder':''}),
            'cnpj': forms.TextInput(attrs={'placeholder':''}),   
            'cpf': forms.TextInput(attrs={'placeholder':''}),                        
            'fazedor_cultura': forms.TextInput(attrs={'placeholder':''}),                        
            'descricao': forms.TextInput(attrs={'placeholder':''}),                        
            'pis': forms.TextInput(attrs={'placeholder':''}),                        
            'banco': forms.TextInput(attrs={'placeholder':''}),                      
            'agencia': forms.TextInput(attrs={'placeholder':''}),                        
            'n_conta': forms.TextInput(attrs={'placeholder':''}),                         
        }        
        exclude = ['tipo_contratacao', 'dt_inclusao', 'user_responsavel']


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
            'qnt': forms.Select(attrs={'class': 'form-control mb-3'}),
            'status': forms.Select(attrs={'class': 'form-control mb-3'}),
            'instagram': forms.TextInput(attrs={'placeholder':'', 'class': 'form-control mb-3'}),
            'facebook': forms.TextInput(attrs={'placeholder':'', 'class': 'form-control mb-3'}),
            'youtube': forms.TextInput(attrs={'placeholder':'', 'class': 'form-control mb-3'}),
        }        
        exclude = ['']