from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from mapeamento_cultural.forms import Form_Anexo_Artista_CPF, Form_Anexo_Artista_CNPJ, Form_Artista, Form_Artista2, Form_ArtistaCNPJ, Form_ArtistaEmpresa, Form_InfoExtra, Form_Usuario
from django.contrib import messages
import os
from cultura.settings import BASE_DIR
from django.contrib.auth.models import User
from mapeamento_cultural.models import Artista, InformacoesExtras, TiposContratação
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
            if len(request.POST['password'])<8:
                senhas=[True, 'Sua senha deve ter pelo menos 8 digitos.']
            elif request.POST['password']!=request.POST['password2']:
                senhas=[True, ' As senhas abaixo não coincidem.']
            else:
                user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
                user.save()
                user.first_name = request.POST['nome']                    
                user.save()
                usuario=form.save()
                usuario.user=user
                usuario.save()
        else:
            print(form.errors)
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
            '2': Form_ArtistaCNPJ,
            '1': Form_Artista
        }
        key=request.POST['tipo_form']        
        form=forms[key](request.POST, request.FILES)
        if form.is_valid():
            try:
                obj=form.save()
                obj.tipo_contratacao=TiposContratação.objects.get(id=key)
                obj.user_responsavel=request.user
                obj.save()                
                messages.add_message(request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso.</b>")                
                return redirect('cad_cult_etapa2', tipo=request.POST['tipo_form'], id=obj.id )
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    context={}
    return render(request, 'cadastro_cultural/etapa_1_artista.html', context)

@login_required
def editar_artista_b(request, id):  
    dados=Artista.objects.get(id=id)
    if dados.tipo_contratacao.id==1:
        form=Form_Artista(instance=dados)
    else:
        form=Form_ArtistaCNPJ(instance=dados)
    if request.method=='POST':      
        if dados.tipo_contratacao.id==1:          
            form=Form_Artista(request.POST, request.FILES, instance=dados)
        else:
            form=Form_ArtistaCNPJ(request.POST, request.FILES, instance=dados)
        if form.is_valid():
            try:
                obj=form.save()                
                messages.add_message(request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso.</b>")                
                return redirect('acc_meus_cadastros_map', id=id)
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    context={
        'form': form,
        'id': id
    }
    return render(request, 'cadastro_cultural/etapa_1_editar.html', context)

@login_required
def editar_artista_c(request, id):  
    dados=Artista.objects.get(id=id)
    form=Form_Artista2(instance=dados)
    if request.method=='POST':                
        form=Form_Artista(request.POST, request.FILES, instance=dados)
        if form.is_valid():
            try:
                obj=form.save()                
                messages.add_message(request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso.</b>")                
                return redirect('acc_meus_cadastros_map', id=id)
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    context={
        'form': form,
        'id': id        
    }
    return render(request, 'cadastro_cultural/etapa_3_editar.html', context)

@login_required
def cadastro_etapa_1_empresa(request):  
    form=Form_ArtistaEmpresa()
    if request.method=='POST':        
        form=Form_ArtistaEmpresa(request.POST, request.FILES)
        if form.is_valid():
            try:
                obj=form.save()
                obj.tipo_contratacao=TiposContratação.objects.get(nome='Contratação por CNPJ_E')
                obj.user_responsavel=request.user
                obj.save()
                messages.add_message(request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso. <br>Aguarde nosso email validando seus dados.</b>")
                return redirect('cad_cult_etapa2', tipo=2, id=obj.id )
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
        'tipo_form':1
    }
    return render(request, 'cadastro_cultural/form.html', context)

@login_required
def get_form_cnpj(request):
    context={
        'form': Form_ArtistaCNPJ(),
        'tipo_form':2
    }
    return render(request, 'cadastro_cultural/form.html', context)

@login_required
def meus_cadastros(request):
    context={
        'cadastros_map_cultural_cpf': Artista.objects.filter(user_responsavel=request.user),
        'cadastros_map_cultural_cnpj': Artista.objects.filter(user_responsavel=request.user)
    }
    return render(request, 'meus_cadastros.html', context)

@login_required
def cadastro_map_cultural_cpf(request, id):

    artista=Artista.objects.get(id=id)
    tipo=artista.tipo_contratacao.nome.split()[-1]
    try:
        info=InformacoesExtras.objects.get(id_artista=id)    
        complemento=True
    except:
        info=[]
        complemento=False
    context={
        'cadastro': artista,       
        'info': info,
        'complemento': complemento,
    }
    return render(request, 'meus_cadastros_detalhes_cpf.html', context)

@login_required
def cadastro_map_cultural_cnpj(request, id):
    artista=Artista.objects.get(id=id)
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
def cadastro_etapa_2(request, id):
    form=Form_InfoExtra(initial={'id_artista': id})
    if request.method=='POST':
        form=Form_InfoExtra(request.POST)
        if form.is_valid():
            obj=form.save()
            obj.id_artista=id
            obj.complete=True
            obj.save()
            return redirect('acc_meus_cadastros_map', id)
    context={
        'form': form,
        'id': id
    }
    return render(request, 'cadastro_cultural/etapa_2.html', context)

@login_required
def admin_cadastros(request):
    context={
        'cadastros_map_cultural_cpf': Artista.objects.all(),
        'cadastros_map_cultural_cnpj': Artista.objects.all()
    }
    return render(request, 'cadastros.html', context)

@login_required
def cadastro_etapa_3(request, id, tipo):
    print(tipo)
    instance=Artista.objects.get(id=id)
    form=Form_Artista2(instance=instance)
    if request.method=='POST':
        form=Form_Artista2(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance=form.save()
            instance.cadastro_completo=True
            form.save()

            return redirect('acc_meus_cadastros_map', id)
    context={
        'form': form,
        'id': id
    }
    return render(request, 'cadastro_cultural/etapa_3.html', context)


@login_required
def cadastro_anexo(request, id, tipo):
    print(tipo)
    instance=Artista.objects.get(id=id)
    if instance.tipo_contratacao.id==1:
        form=Form_Anexo_Artista_CPF(instance=instance)
    else:
        form=Form_Anexo_Artista_CNPJ(instance=instance)
    if request.method=='POST':
        form=Form_Anexo_Artista_CPF(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            isntance=form.save()
            form=Form_Anexo_Artista_CPF(instance=instance)
            context={
                'form': form,
                'id': id,
                'success': ['bg-success', 'Anexo enviado com sucesso!']
            }
            return render(request, 'cadastro_cultural/anexos.html', context)
    context={
        'form': form,
        'id': id,
        'success': ['', '']
    }
    return render(request, 'cadastro_cultural/anexos.html', context)

@login_required
def editar_etapa_2(request, id):
    instance=InformacoesExtras.objects.get(id_artista=id)
    form=Form_InfoExtra(instance=instance)
    if request.method=='POST':
        form=Form_InfoExtra(request.POST, instance=instance)
        if form.is_valid():
            obj=form.save()            
            obj.save()
            return redirect('acc_meus_cadastros_map', id)
    context={
        'form': form,
        'id': id

    }
    return render(request, 'cadastro_cultural/etapa_2.html', context)
