from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mapeamento_cultural.forms import Form_Artista, Form_ArtistaCNPJ, Form_Usuario
from django.contrib import messages
import os
from cultura.settings import BASE_DIR
from mapeamento_cultural.models import TiposContratação

# Create your views here.
def index(request):
    return render(request, 'index.html')

def mapeamento_cultural(request):
    return render(request, 'mapeamento.html')

def lei866(request):
    return render(request, 'lei866.html')

def cadastro_usuario(request):
    form=Form_Usuario()
    senhas=False
    nome=''
    if request.method=='POST':
        nome=request.POST['nome']
        form=Form_Usuario(request.POST)
        if form.is_valid():            
            if len(request.POST['senha'])<8:
                senhas=[True, 'Sua senha deve ter pelo menos 8 digitos.']
            elif request.POST['senha']!=request.POST['senha2']:
                senhas=[True, ' As senhas abaixo não coincidem.']

    context={
        'form': form,
        'error_senha': senhas,
        'nome': nome
    }
    return render(request, 'admin/cadastrar-se.html', context)

@login_required(login_url='/admin/login')
def cadastro_etapa_1(request):
    return render(request, 'cadastro_cultural/etapa_1.html')

@login_required
def cadastro_etapa_1_artista(request):  
    if request.method=='POST':        
        forms={
            'cnpj': Form_ArtistaCNPJ,
            'cpf': Form_Artista
        }
        key=request.POST['tipo_form']        
        form=forms[key](request.POST, request.FILES)
        if form.is_valid():
            try:
                obj=form.save()
                obj.tipo_contratacao=TiposContratação.objects.get(nome='Contratação por '+key)
                obj.user_responsavel=request.user
                obj.save()
                messages.add_message(request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso. <br>Aguarde nosso email validando seus dados.</b>")
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    context={}
    return render(request, 'cadastro_cultural/etapa_1_artista.html', context)

@login_required
def get_form_cpf(request):
    context={
        'form': Form_Artista(),
        'tipo_form':'cpf'
    }
    return render(request, 'cadastro_cultural/form.html', context)

@login_required
def get_form_cnpj(request):
    context={
        'form': Form_ArtistaCNPJ(),
        'tipo_form':'cnpj'
    }
    return render(request, 'cadastro_cultural/form.html', context)