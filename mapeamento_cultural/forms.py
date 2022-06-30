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
        }        
        exclude = ['cnpj', 'tipo_contratacao', 'dt_inclusao', 'user_responsavel']

class Form_ArtistaCNPJ(ModelForm):
    class Meta:
        model = ArtistaContratoCNPJ
        widgets = {
            # 'nome_artistico': forms.EmailInput(attrs={'placeholder':''}),
            'cnpj': forms.TextInput(attrs={'placeholder':''}),                        
        }        
        exclude = ['tipo_contratacao', 'dt_inclusao', 'user_responsavel']