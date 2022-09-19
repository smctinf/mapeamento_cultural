from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

from .models import Log_anexos, Recibos, Usuario
from mapeamento_cultural.forms import Form_Anexo_Artista_CPF, Form_Anexo_Artista_CNPJ, Form_Artista, Form_Artista2, Form_ArtistaCNPJ, Form_ArtistaEmpresa, Form_InfoExtra_CPF, Form_InfoExtra_CNPJ, Form_Recibos, Form_Usuario


from django.contrib import messages
import os
from cultura.settings import BASE_DIR
from mapeamento_cultural.models import Artista, InformacoesExtras, TiposContratação
from qr_code.qrcode.utils import QRCodeOptions

# Create your views here.


def index(request):
    return render(request, 'index.html')


def mapeamento_cultural(request):
    context = {
        "artista": False
    }

    try:
        artista = Artista.objects.filter(user_responsavel=request.user)
    except:
        artista = []
    
    if len(artista) > 0:    
        context = {
            "artista": True
        }
        # return redirect('acc_meus_cadastros')

    return render(request, 'mapeamento.html', context)


def lei866(request):
    return render(request, 'lei866.html')


def cadastro_usuario(request):
    form = Form_Usuario()
    senhas = False
    nome = ''
    if request.method == 'POST':
        nome = request.POST['nome']
        form = Form_Usuario(request.POST)
        if form.is_valid():
            if len(request.POST['password']) < 8:
                senhas = [True, 'Sua senha deve ter pelo menos 8 digitos.']
            elif request.POST['password'] != request.POST['password2']:
                senhas = [True, ' As senhas abaixo não coincidem.']
            else:
                try:
                    user = User.objects.create_user(
                        username=request.POST['email'], email=request.POST['email'], password=request.POST['password'])
                    user.first_name = request.POST['nome']
                    user.set_password(request.POST['password'])
                    user.save()
                    usuario = form.save()
                    usuario.user = user
                    usuario.save()
                    messages.add_message(
                        request, messages.SUCCESS, "<b class='text-success'>Usuário cadastrado com sucesso</b>")
                    return redirect('login')
                except Exception as e:
                    print(e)

        else:
            print(form.errors)
    context = {
        'form': form,
        'error_senha': senhas,
        'nome': nome
    }
    return render(request, 'admin/cadastrar-se.html', context)

@login_required
def cadastro_etapa_1(request):
    context = {
    "artista": False 
    }

    try:
        artista = Artista.objects.get(user_responsavel=request.user)
    except:
        artista = None
    if artista:
        context = {
            "artista": True
        }

    if request.method == 'POST':
        forms = {
            '2': Form_ArtistaCNPJ,
            '1': Form_Artista
        }
        key = request.POST['tipo_form']
        form = forms[key](request.POST, request.FILES)
        if form.is_valid():
            try:
                obj = form.save()
                obj.tipo_contratacao = TiposContratação.objects.get(id=key)
                obj.user_responsavel = request.user
                obj.save()
                messages.add_message(
                    request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso.</b>")
                return redirect('acc_meus_cadastros')
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    return render(request, 'cadastro_cultural/mapeamento_cadastro_inicial.html', context)

@login_required
def cadastro_cnpj(request):
    context = {
    "artista": False,
    'form': Form_ArtistaCNPJ(),
    }

    if request.method == 'POST':                
        form = Form_ArtistaCNPJ(request.POST, request.FILES)
        if form.is_valid():
            try:
                obj = form.save()
                obj.tipo_contratacao = TiposContratação.objects.get(id=2)
                obj.user_responsavel = request.user
                obj.save()
                messages.add_message(
                    request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso.</b>")
                print("ta pronto para redirecionar")
                return redirect('acc_meus_cadastros')
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    return render(request, 'cadastro_cultural/mapeamento_cadastro.html', context)

@login_required
def cadastro_cpf(request):
    context = {
    "artista": False,
    'form': Form_Artista(),
    'tipo_cadastro': 1
    }

    if request.method == 'POST':                
        form = Form_Artista(request.POST, request.FILES)
        if form.is_valid():
            try:
                obj = form.save()
                obj.tipo_contratacao = TiposContratação.objects.get(id=1)
                obj.user_responsavel = request.user
                obj.save()
                messages.add_message(
                    request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso.</b>")
                return redirect('cad_cult_etapa2', obj.id)
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    return render(request, 'cadastro_cultural/mapeamento_cadastro.html', context)

@login_required
def editar_artista_b(request, id):
    dados = Artista.objects.get(id=id, user_responsavel=request.user)
    if dados.tipo_contratacao.id == 1:
        form = Form_Artista(instance=dados)
    else:
        form = Form_ArtistaCNPJ(instance=dados)
    if request.method == 'POST':
        if dados.tipo_contratacao.id == 1:
            form = Form_Artista(request.POST, request.FILES, instance=dados)
        else:
            form = Form_ArtistaCNPJ(
                request.POST, request.FILES, instance=dados)
        if form.is_valid():
            try:
                obj = form.save()
                messages.add_message(
                    request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso.</b>")
                return redirect('acc_meus_cadastros_map', id)
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    context = {
        'form': form,
        'id': id
    }
    return render(request, 'cadastro_cultural/etapa_1_editar.html', context)


@login_required
def editar_artista_c(request, id):
    dados = Artista.objects.get(id=id, user_responsavel=request.user)
    form = Form_Artista2(instance=dados)
    if request.method == 'POST':
        form = Form_Artista2(request.POST, request.FILES, instance=dados)
        if form.is_valid():
            try:
                dados = form.save()
                messages.add_message(
                    request, messages.SUCCESS, "<b class='text-success'>Cadastro alterado com sucesso.</b>")
                return redirect('acc_meus_cadastros_map', id)
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            print(form.errors)
            form = Form_Artista2(instance=dados)
            print('error2')
            messages.add_message(request, messages.ERROR, form.errors)
            print('error3')
    context = {
        'form': form,
        'id': id
    }
    return render(request, 'cadastro_cultural/etapa_3_editar.html', context)


@login_required
def cadastro_etapa_1_empresa(request):
    form = Form_ArtistaEmpresa()
    if request.method == 'POST':
        form = Form_ArtistaEmpresa(request.POST, request.FILES)
        if form.is_valid():
            try:
                obj = form.save()
                obj.tipo_contratacao = TiposContratação.objects.get(
                    nome='Contratação por CNPJ_E')
                obj.user_responsavel = request.user
                obj.save()
                messages.add_message(
                    request, messages.SUCCESS, "<b class='text-success'>Cadastro realizado com sucesso. <br>Aguarde nosso email validando seus dados.</b>")
                return redirect('cad_cult_etapa2', tipo=2, id=obj.id)
            except Exception as E:
                print(E)
                messages.add_message(request, messages.ERROR, form.errors)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    context = {
        'form': form
    }
    return render(request, 'cadastro_cultural/etapa_1_empresario.html', context)


@login_required
def get_form_cpf(request):
    context = {
        'form': Form_Artista(),
        'tipo_form': 1
    }
    return render(request, 'cadastro_cultural/form.html', context)


@login_required
def get_form_cnpj(request):
    context = {
        'form': Form_ArtistaCNPJ(),
        'tipo_form': 2
    }
    return render(request, 'cadastro_cultural/form.html', context)


@login_required
def meus_cadastros(request):
    print(request.user)
    cad_cpf=Artista.objects.filter(user_responsavel=request.user, tipo_contratacao__nome='Contratação por CPF')
    cad_cnpj=Artista.objects.filter(user_responsavel=request.user, tipo_contratacao__nome='Contratação por CNPJ')
    if len(cad_cpf)==0:
        cadastrar_cpf=True
    else: 
        cadastrar_cpf=False
    context = {
        'cadastros_map_cultural_cpf': cad_cpf,
        'cadastros_map_cultural_cnpj': cad_cnpj,
        'cpf': cadastrar_cpf,
    }
    return render(request, 'meus_cadastros.html', context)


@login_required
def meu_perfil(request):
    print(request.user)
    context = {
        'usuario': Usuario.objects.get(user=request.user),
    }
    return render(request, 'meu_perfil.html', context)


@login_required
def cadastro_map_cultural_cpf(request, id):

    try:
        artista = Artista.objects.get(id=id, user_responsavel=request.user)
        tipo = artista.tipo_contratacao.nome.split()[-1]
    except:
        if request.user.is_superuser:
            artista = Artista.objects.get(id=id)
            tipo = artista.tipo_contratacao.nome.split()[-1]
        else:
            raise PermissionDenied()
    try:
        info = InformacoesExtras.objects.get(id_artista=artista.id)
        complemento = True
    except:
        info = []
        complemento = False
    context = {
        'cadastro': artista,
        'info': info,
        'complemento': complemento,
        'usuario': Usuario.objects.get(user=request.user),
        'tipo': tipo
    }
    return render(request, 'meus_cadastros_detalhes_cpf.html', context)

@login_required
def excluir_map_cultural(request, id):
    try:
        artista = Artista.objects.get(id=id, user_responsavel=request.user)
        artista.delete()
        messages.add_message(request, messages.SUCCESS, "<b class='text-success'>Cadastro excluído com sucesso.</b>")
        return redirect('acc_meus_cadastros')
    except Exception as E:
        print(E)
        messages.add_message(request, messages.ERROR, "<b class='text-danger'>Erro ao excluir cadastro.</b>")
        return redirect('acc_meus_cadastros')

@login_required
def cadastro_map_cultural_cnpj(request, id):
    print("ESTOU NO DE CNPJ")
    artista = Artista.objects.get(id=id)
    tipo = artista.tipo_contratacao.nome.split()[-1]
    try:
        info = InformacoesExtras.objects.get(tipo=tipo.lower(), id_artista=id)
    except:
        info = []
    context = {
        'cadastro': artista,
        'info': info
    }
    return render(request, 'meus_cadastros_detalhes_cnpj.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/login')
    else:
        return redirect('/')


def login_view(request):
    context = {}
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
            context = {
                'error': True,
            }

    return render(request, 'admin/login.html', context)


@login_required
def cadastro_etapa_2(request, id):
    artista=Artista.objects.get(id=id, user_responsavel=request.user)
    id = artista.id
    if artista.tipo_contratacao.id==1:
        form = Form_InfoExtra_CPF(initial={'id_artista': id})
    elif artista.tipo_contratacao.id==2:
        form = Form_InfoExtra_CNPJ(initial={'id_artista': id})
    if request.method == 'POST':
        if artista.tipo_contratacao.id==1:
            form = Form_InfoExtra_CPF(request.POST)
        elif artista.tipo_contratacao.id==2:
            form = Form_InfoExtra_CNPJ(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.id_artista = id
            obj.complete = True
            obj.save()
            return redirect('acc_meus_cadastros_map', id)
    context = {
        'form': form,
        'id': id
    }
    return render(request, 'cadastro_cultural/etapa_2.html', context)


@login_required
def admin_cadastros(request):
    context = {
        'cadastros_map_cultural_cpf': Artista.objects.all(),
        'cadastros_map_cultural_cnpj': Artista.objects.all()
    }
    return render(request, 'cadastros.html', context)


@login_required
def cadastro_etapa_3(request, id):
    instance = Artista.objects.get(id=id, user_responsavel=request.user)
    form = Form_Artista2(instance=instance)
    if request.method == 'POST':
        form = Form_Artista2(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save()
            instance.cadastro_completo = True
            form.save()

            return redirect('acc_meus_cadastros_map', id)
    context = {
        'form': form,
        'id': id
    }
    return render(request, 'cadastro_cultural/etapa_3.html', context)


@login_required
def cadastro_anexo(request, id):
    '''
    CPF -> instance.tipo_contratacao.id == 1
    CNPJ -> instance.tipo_contratacao.id == 2
    '''

    try:
        instance = Artista.objects.get(id=id, user_responsavel=request.user)        
    except:
        if request.user.is_superuser:
            instance = Artista.objects.get(id=id)            
        else:
            raise PermissionDenied()
    
    try:
        recibos=Recibos.objects.filter(artista=instance)
    except:
        recibos=[]
    if instance.tipo_contratacao.id == 1:
        form = Form_Anexo_Artista_CPF(instance=instance)
        anexos = [
            'file_cpf',
            'file_comprovante_residencia',
            'file_pis',
            'comprovante_de_cc',
            'declaracao_n_viculo',
            'comprovante_iss',
            'portfolio',
            'rg'
            
        ]
    else:
        form = Form_Anexo_Artista_CNPJ(instance=instance)
        anexos = [
            'prova_inscricao_PJ_nacional',
            'file_comprovante_residencia',
            'file_pis',
            'comprovante_de_cc',
            'declaracao_n_viculo',
            'comprovante_iss',            
            'certidao_negativa_debitos_relativos',
            'certidao_regularidade_icms',
            'certidao_regularidade_iss',
            'certidao_negativa_debitos',
            'certidao_regularidade_situacao',
            'certidao_negativa_debitos_trabalhistas',
            'documento_empresario_exclusivo'
            'portfolio',
            'rg'
        ]
    lista = []
    form_recibos=Form_Recibos()
    if request.method == 'POST':
        if request.user == instance.user_responsavel:
            if instance.tipo_contratacao.id == 1:
                form = Form_Anexo_Artista_CPF(request.POST, request.FILES, instance=instance)
            else:
                form = Form_Anexo_Artista_CNPJ(request.POST, request.FILES, instance=instance)
            
            keys=request.FILES.keys()
            if 'comprovante' in keys:
                form_recibos=Form_Recibos(request.POST, request.FILES)
                if form_recibos.is_valid():
                    obj = form_recibos.save()
                    obj.artista = instance
                    obj.save() 
                    if instance.tipo_contratacao.id == 1:
                        form = Form_Anexo_Artista_CPF(instance=instance)     
                    else:
                        form = Form_Anexo_Artista_CNPJ(instance=instance)
                    for a in anexos:
                        lista.append([a, instance.__dict__[a].name != ''])
                    log=Log_anexos(artista=instance, anexo='comprovante',filename=request.FILES['comprovante'].name, user_responsavel=request.user)
                    log.save()
                    context = {
                        'form': form,
                        'lista': lista,
                        'success': ['bg-success', 'Anexo enviado com sucesso!'],
                        'id': id,
                        'recibos': recibos,
                        'bg_recibos': '[SEM ANEXO]' if len(recibos)==0 else '[ANEXADO]',
                        'form_recibos': form_recibos
                    }                
        
                
            if form.is_valid():
                instance = form.save()
                if instance.tipo_contratacao.id == 1:
                    form = Form_Anexo_Artista_CPF(instance=instance)     
                else:
                    form = Form_Anexo_Artista_CNPJ(instance=instance)            
                for a in anexos:
                    lista.append([a, instance.__dict__[a].name != ''])
                
                for i in keys:
                    log=Log_anexos(artista=instance, anexo=i, filename=request.FILES[i].name, user_responsavel=request.user)
                    log.save()
                context = {
                    'form': form,
                    'lista': lista,
                    'success': ['bg-success', 'Anexo enviado com sucesso!'],
                    'id': id,
                    'recibos': recibos,
                    'bg_recibos': '[SEM ANEXO]' if len(recibos)==0 else '[ANEXADO]',
                    'form_recibos': form_recibos
                }
        else:
            raise PermissionDenied()

    else:
        for a in anexos:
            lista.append([a, instance.__dict__[a].name != ''])
        context = {
            'form': form,
            'lista': lista,
            'success': ['', ''],
            'id': id,
            'recibos': recibos,
            'form_recibos': form_recibos,
            'bg_recibos': '[SEM ANEXO]' if len(recibos)==0 else '[ANEXADO]',
            'log': Log_anexos.objects.filter(artista=instance)
        }
    return render(request, 'cadastro_cultural/anexos.html', context)


@login_required
def editar_etapa_2(request, id):
    artista = Artista.objects.get(id=id, user_responsavel=request.user)
    instance = InformacoesExtras.objects.get(id_artista=artista.id)
    if artista.tipo_contratacao.id==1:
        form = Form_InfoExtra_CPF(instance=instance)
    elif artista.tipo_contratacao.id==2:
        form = Form_InfoExtra_CNPJ(instance=instance)
    if request.method == 'POST':
        if artista.tipo_contratacao.id==1:
            form = Form_InfoExtra_CPF(request.POST, instance=instance)
        elif artista.tipo_contratacao.id==2:
            form = Form_InfoExtra_CNPJ(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save()
            return redirect('acc_meus_cadastros_map', id)
    context = {
        'form': form,
        'id': id
    }
    return render(request, 'cadastro_cultural/etapa_2.html', context)


@login_required
def change_password(request):
    status = ['', '']
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante!
            status = ['bg-success text-white py-1 text-center',
                      'Senha alterada.']
            form = PasswordChangeForm(request.user)
        else:
            status = ['bg-danger text-white',
                      'Você deve cumprir todos os requisitos para alterar sua senha.']
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
        'status': status
    }
    return render(request, 'change_password.html', context)


@login_required
def alterar_meus_dados(request):
    usuario = Usuario.objects.get(user=request.user)
    context = {
        'usuario': usuario,
        'form': Form_Usuario(instance=usuario),
    }
    if request.method == 'POST':
        form = Form_Usuario(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "<b class='text-success'>Dados alterado com sucesso.</b>")
            usuario = Usuario.objects.get(user=request.user)
            context = {
                'usuario': usuario,
                'form': Form_Usuario(instance=usuario),
            }

    return render(request, 'alterar_meus_dados.html', context)

@login_required
def deletar_anexo(request, id):
    
    if request.method == 'POST':
        recibo=Recibos.objects.get(id=id)
        if request.user==recibo.artista.user_responsavel:
            recibo.delete()
        else:
            raise PermissionDenied()
    return HttpResponse(status=200)  