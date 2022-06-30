from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mapeamento_cultural.forms import Form_Artista, Form_Usuario
from django.contrib import messages
import os
from cultura.settings import BASE_DIR

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
    print(os.path.join(BASE_DIR, 'cultura/media'))
    form=Form_Artista()
    if request.method=='POST':
        form=Form_Artista(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Cadastro realizado com sucesso. <br>Aguarde nosso email validando seus dados.')
            except Exception as E:
                print(E)
    context={
        'form': form
    }
    return render(request, 'cadastro_cultural/etapa_1_artista.html', context)

@login_required
def get_form_cpf(request):
    context={
        'form': Form_Artista()
    }
    return render(request, 'cadastro_cultural/form.html', context)