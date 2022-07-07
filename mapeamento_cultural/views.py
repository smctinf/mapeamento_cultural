from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from mapeamento_cultural.forms import Form_Artista, Form_ArtistaCNPJ, Form_ArtistaEmpresa, Form_InfoExtra, Form_Usuario
from django.contrib import messages
import os
from cultura.settings import BASE_DIR
from mapeamento_cultural.models import ArtistaContratoCNPJ, ArtistaContratoCPF, InformacoesExtras, TiposContratação
from qr_code.qrcode.utils import QRCodeOptions

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

@login_required
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
                obj.tipo_contratacao=TiposContratação.objects.get(nome='Contratação por '+key.upper())
                obj.user_responsavel=request.user
                obj.save()                
                messages.add_message(request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso. <br>Aguarde nosso email validando seus dados.</b>")                
                return redirect('cad_cult_etapa2', tipo=request.POST['tipo_form'], id=obj.id )
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    context={}
    return render(request, 'cadastro_cultural/etapa_1_artista.html', context)

@login_required
def editar_cpf_artista(request, id):  
    dados=ArtistaContratoCPF(id=id)
    form=Form_Artista(instance=dados)
    if request.method=='POST':                
        form=Form_Artista(request.POST, request.FILES, instance=dados)
        if form.is_valid():
            try:
                obj=form.save()                
                messages.add_message(request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso. <br>Aguarde nosso email validando seus dados.</b>")                
                return redirect('acc_meus_cadastros_map_cpf', id=obj.id)
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    context={}
    return render(request, 'cadastro_cultural/etapa_1_artista.html', context)

@login_required
def cadastro_etapa_1_empresa(request):  
    form=Form_ArtistaEmpresa()
    if request.method=='POST':        
        form=Form_ArtistaEmpresa(request.POST, request.FILES)
        if form.is_valid():
            try:
                obj=form.save()
                obj.tipo_contratacao=TiposContratação.objects.get(nome='Contratação por CNPJ')
                obj.user_responsavel=request.user
                obj.save()
                messages.add_message(request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso. <br>Aguarde nosso email validando seus dados.</b>")
                return redirect('cad_cult_etapa2', tipo='cnpj_e', id=obj.id )
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    context={
        'form': form
    }
    return render(request, 'cadastro_cultural/etapa_1_empresario.html', context)

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

@login_required
def meus_cadastros(request):
    context={
        'cadastros_map_cultural_cpf': ArtistaContratoCPF.objects.filter(user_responsavel=request.user),
        'cadastros_map_cultural_cnpj': ArtistaContratoCNPJ.objects.filter(user_responsavel=request.user)
    }
    return render(request, 'meus_cadastros.html', context)

@login_required
def cadastro_map_cultural_cpf(request, id):

    artista=ArtistaContratoCPF.objects.get(id=id)
    tipo=artista.tipo_contratacao.nome.split()[-1]
    try:
        info=InformacoesExtras.objects.get(tipo=tipo.lower(), id_artista=id)    
    except:
        info=[]
    context={
        'cadastro': artista,       
        'info': info 
    }
    return render(request, 'meus_cadastros_detalhes_cpf.html', context)

@login_required
def cadastro_map_cultural_cnpj(request, id):
    artista=ArtistaContratoCNPJ.objects.get(id=id)
    tipo=artista.tipo_contratacao.nome.split()[-1]
    try:
        info=InformacoesExtras.objects.get(tipo=tipo.lower(), id_artista=id)    
    except:
        info=[]
    context={
        'cadastro': artista,       
        'info': info 
    }
    return render(request, 'meus_cadastros_detalhes_cnpj.html', context)

@login_required
def logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/logout')
    else:
        return redirect('/login')

def login_view(request):
    context={}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)            
            if "next" in request.GET:
                return redirect(request.GET.get('next'))
            return redirect('/')
        else:                
            context={
                'error': True,    
            }
    
    return render(request, 'admin/login.html', context)

@login_required
def cadastro_etapa_2(request, id, tipo):
    form=Form_InfoExtra(initial={'tipo': tipo, 'id_artista': id})
    if request.method=='POST':
        form=Form_InfoExtra(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cad_cult_etapa1')
    context={
        'form': form

    }
    return render(request, 'cadastro_cultural/etapa_2.html', context)
