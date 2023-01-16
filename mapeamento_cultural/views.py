from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.http import HttpResponse

from .models import Area_Atuacao, Log_anexos, Recibos, Usuario
from mapeamento_cultural.forms import Form_Anexo_Artista_CPF, Form_Anexo_Artista_CNPJ, Form_Artista, Form_Artista2, Form_ArtistaCNPJ, Form_ArtistaEmpresa, Form_InfoExtra_CPF, Form_InfoExtra_CNPJ, Form_Recibos, Form_Usuario, Form_Validade_Anexo_Artista_CNPJ, Form_Validade_Anexo_Artista_CPF


from django.contrib import messages
from cultura.settings import BASE_DIR
from mapeamento_cultural.models import Artista, InformacoesExtras, TiposContratação
from django.core.mail import EmailMessage,  EmailMultiAlternatives, send_mail

# Create your views here.
import numpy as np
import pandas as pd


# @login_required
# def enviar_email(request):

#     fazedores_de_cultura = Artista.objects.all()
#     for artista in fazedores_de_cultura:
#         try:

#             subject= f'Cadastro Fazedor de Cultura Nova Friburgo'
#             from_email = settings.EMAIL_HOST_USER
#             to = [artista.user_responsavel.email]
#             text_content = 'This is an important message.'
#             html_content = f"""
            
#             <b>Atenção artistas produtores culturais, profissionais de arte e cultura, queremos conhecer você!</b>

#             <p> A Secretaria Municipal de Cultura de Nova Friburgo realiza o cadastro de artistas dos mais variados segmentos. A ação faz parte de um mapeamento que a pasta está desenvolvendo para gerar dados e informações capazes de pensar as políticas públicas culturais. As inscrições são contínuas.</p>
             
#             <p>Os artistas já cadastrados no mapeamento realizado para recebimento dos recursos da Lei Aldir Blanc poderão editar e atualizar suas informações. Pra realizar o primeiro acesso o usuário deverá inserir no campo 'usuário' o seu email de cadastro no mapeamento 2020 e sua senha é composta somente pelos números do seu CPF. Podem se cadastrar toda e qualquer pessoa física atuante na área cultural em Nova Friburgo. Se você conhece algum fazedor de cultura na cidade repasse essas informações para que consigamos atingir o maior número de artistas.</p>

#             <p>Qualquer dúvida pode ser encaminha para o email mapeamentoculturalnf@gmail.com ou mesmo pelo telofone (22) 2521-1558</p>
#             <br/><p> Atenciosamente, </p> <p>Equipe da Secretaria Municipal de Cultura</p>
#              </br>
#              <div>
#             <img src="https://culturanf.novafriburgo.rj.gov.br/static/images/logo_pmnf_cultura.png"/>
#              </div>
#              """

#             msg = EmailMultiAlternatives(subject, text_content, from_email, to)
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()

#         except Exception as E:
#             print(E)
#             return HttpResponse(E)
#         else:
#             print('email enviado com sucesso!')
#     return HttpResponse('deu certo')


def index(request):
    return render(request, 'index.html')


def mapeamento_listagem(request):
    busca=False    
    filtro_template={}
    area_atuacao=Area_Atuacao.objects.all()
    if request.method=='POST':
        filtro=[]        
        # print(request.POST)
        # if request.POST['ordem_area']!='':
        #     if request.POST['ordem_area']=='Artes Cênicas' and request.POST['ordem']=='crescente':
        #         ordem=['fazedor_cultura', 'fazedor_cultura_cnpj']
        #     elif request.POST['ordem_area']=='Artes Cênicas' and request.POST['ordem']=='decrescente':
        #         ordem=['-fazedor_cultura', '-fazedor_cultura_cnpj']
        # else:
        #     ordem='id'
        for i in request.POST:
            if request.POST[i]!='' and i!='csrfmiddlewaretoken' and i!='ordem':                
                busca=True
                filtro.append([i,request.POST[i]])
                filtro_template[i]=True
        if busca:
            if request.POST['area_atuacao']!='' and request.POST['tipo_inscricao']!='':            
                artista=Artista.objects.filter(area=request.POST['area_atuacao'], tipo_contratacao=request.POST['tipo_inscricao'])
            elif request.POST['area_atuacao']!='' and request.POST['tipo_inscricao']=='':      
                artista=Artista.objects.filter(area=request.POST['area_atuacao'])
            elif request.POST['area_atuacao']=='' and request.POST['tipo_inscricao']!='':      
                artista=Artista.objects.filter(tipo_contratacao=request.POST['tipo_inscricao'])
        else:
            busca=True
            artista=Artista.objects.all()    
    else:
        artista=Artista.objects.all()
    context={
        'algo': artista,
        'busca': busca,
        'area_atuacao':area_atuacao,
    }
    return render(request, 'mapeamento_listagem.html', context)

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
    dados = Artista.objects.get(id=id)
    if dados.user_responsavel != request.user:
        raise PermissionDenied()  
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
    dados = Artista.objects.get(id=id)
    if dados.user_responsavel != request.user:
        raise PermissionDenied()  
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

    print(request.user)
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
    artista=Artista.objects.get(id=id)
    if artista.user_responsavel != request.user:
        raise PermissionDenied()  
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
    instance = Artista.objects.get(id=id)
    if instance.user_responsavel != request.user:
        raise PermissionDenied()    
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
        instance = Artista.objects.get(id=id)        
        if instance.user_responsavel != request.user:
            raise PermissionDenied()  
    except:
        raise PermissionDenied()  
        # if request.user.is_superuser:
        #     instance = Artista.objects.get(id=id)            
        # else:
        #     raise PermissionDenied()
    
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
            'documento_empresario_exclusivo',
            'portfolio',
            'rg'
        ]
    lista = []
    form_recibos=Form_Recibos()
    form_validade=""

    if instance.tipo_contratacao.id == 1:
        form_validade = Form_Validade_Anexo_Artista_CPF(instance=instance)
    else:
        form_validade = Form_Validade_Anexo_Artista_CNPJ(instance=instance)
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
                        'form_recibos': form_recibos,
                        'validade':form_validade
                        
                    }                
        
                
            if form.is_valid():
                instance = form.save()
                if instance.tipo_contratacao.id ==1:
                    form_validade = Form_Validade_Anexo_Artista_CPF(request.POST, instance=instance)
                else:
                    form_validade = Form_Validade_Anexo_Artista_CNPJ(request.POST, instance=instance)
                if form_validade.is_valid():

                    if instance.tipo_contratacao.id == 1:
                        form = Form_Anexo_Artista_CPF(instance=instance)     
                    else:
                        form = Form_Anexo_Artista_CNPJ(instance=instance)            
                    for a in anexos:
                        lista.append([a, instance.__dict__[a].name != ''])
                    
                    for i in keys:
                        log=Log_anexos(artista=instance, anexo=i, filename=request.FILES[i].name, user_responsavel=request.user)
                        log.save()
                    form_validade.save()
                    context = {
                        'form': form,
                        'lista': lista,
                        'success': ['bg-success', 'Anexo enviado com sucesso!'],
                        'id': id,
                        'recibos': recibos,
                        'bg_recibos': '[SEM ANEXO]' if len(recibos)==0 else '[ANEXADO]',
                        'form_recibos': form_recibos,
                        'validade':form_validade
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
            'log': Log_anexos.objects.filter(artista=instance),
            'validade':  form_validade
        }
    return render(request, 'cadastro_cultural/anexos.html', context)


@login_required
def editar_etapa_2(request, id):
    artista = Artista.objects.get(id=id)
    if artista.user_responsavel != request.user:
        raise PermissionDenied()  
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


@login_required
def auxiliar(request):
    url=str(BASE_DIR) +'/cultura/static/dados.csv'

    colunas_de_interesse={
        'dt_inclusao': 'Carimbo de data/hora',
        #user
        'nome': 'NOME COMPLETO:',
        'cpf': 'CPF:',
        'data_nascimento' : 'DATA DE NASCIMENTO:',
        'email': 'Endereço de e-mail',
        # 'endereco',
        # 'bairro',        
        #informacoes extras
        'descricao': 'FAÇA UM BREVE HISTÓRICO DE SUAS ATIVIDADES CULTURAIS DESENVOLVIDAS NOS ÚLTIMOS ANOS (2018, 2019, 2020)',
        #'endereco',
        #artista
        'tipo_contratacao': 'Desejo fazer cadastro de:',
        'fazedor_cultura': 'NOME ARTÍSTICO:',
        'telefone': 'TELEFONE celular/WhatsApp:',
        'pis': 'PIS/PASEP/NIT:',
        'fazedor_cultura_cnpj': 'NOME FANTASIA (caso exista):',
        'cnpj': 'CNPJ:',
        'area': 'EM QUAL SEGMENTO, GRUPO, CATEGORIA E/OU LINGUAGEM ARTÍSTICA VOCÊ ESTÁ INSERIDO?'
    }

    area_atuacao=[
        'EM QUAL SEGMENTO, GRUPO, CATEGORIA E/OU LINGUAGEM ARTÍSTICA VOCÊ ESTÁ INSERIDO?',
    ]
    lista_colunas_de_interesse=[
        'Carimbo de data/hora',
        'NOME COMPLETO:',
        'CPF:',
        'DATA DE NASCIMENTO:',
        'Endereço de e-mail',
        # 'endereco',
        # 'bairro',        
        #informacoes extras
        'FAÇA UM BREVE HISTÓRICO DE SUAS ATIVIDADES CULTURAIS DESENVOLVIDAS NOS ÚLTIMOS ANOS (2018, 2019, 2020)',
        #'endereco',
        #artista
        'Desejo fazer cadastro de:',
        'NOME ARTÍSTICO:',
        'TELEFONE celular/WhatsApp:',
        'PIS/PASEP/NIT:',
        'NOME FANTASIA (caso exista):',
        'CNPJ:',
        'EM QUAL SEGMENTO, GRUPO, CATEGORIA E/OU LINGUAGEM ARTÍSTICA VOCÊ ESTÁ INSERIDO?'
    ]

    df=pd.read_csv(url)
    df.drop('Unnamed: 2', inplace=True, axis=1)
    df.drop('VOCÊ É TITULAR DE BENEFÍCIO PREVIDENCIÁRIO, ASSISTENCIAL, DE SEGURO DESEMPREGO, DO AUXÍLIO EMERGENCIAL PREVISTO PELA LEI 13982 DE 2/4/2020 OU PROGRAMA DE TRANSFERÊNCIA DE RENDA FEDERAL (RESSALVADO O PROGRAMA BOLSA FAMÍLIA)?', inplace=True, axis=1)
    df.drop('SUA RENDA FAMILIAR MENSAL POR PESSOA É DE ATÉ MEIO SALÁRIO MÍNIMO (R$ 552,50)? (De acordo com Art. 6º, inciso IV da Lei 14.017, 29 de junho de 2020)', inplace=True, axis=1)
    df.drop('SUA RENDA FAMILIAR MENSAL TOTAL, OU SEJA, SOMANDO O SALÁRIO DE TODOS DA RESIDÊNCIA É DE ATÉ 03 (TRÊS) SALÁRIOS MÍNIMOS (R$3.135,00)? (De acordo com Art. 6º, inciso IV da Lei 14.017, 29 de junho de 2020)', inplace=True, axis=1)
    df.drop('VOCÊ REALIZOU DECLARAÇÃO DE IMPOSTO DE RENDA, EM 2018, INFORMANDO RENDA SUPERIOR A R$: 28.559,70 (vinte e oito mil, quinhentos e cinquenta e nove reais e setenta centavos)? (De acordo com Art. 6º, inciso V daLei 14.017, 29 de junho de 2020)', inplace=True, axis=1)
    # df_=df.drop_duplicates(area_atuacao[0])
    df_=df.sort_values(by=[area_atuacao[0]])
    df_=df_.drop_duplicates(area_atuacao[0])
    
    dados=df.loc[:, lista_colunas_de_interesse]
    # dados=df
    #área de atuação
    dados_area_atuacao=df_.loc[:, area_atuacao]   
    # for dado_atuacao in dados_area_atuacao[dados_area_atuacao.columns[0]]:
            # print(dado_atuacao)

    cont=0
    cont_fisica=0
    cont_artista=0
    cont_erro_artista=0
    cont_erro_user=0
    cont_usuarios_cadastrados=0
    error_area=[]
    if True:
        for i in range(357):
            d={'endereco': 'NaN', 'bairro': 'NaN'}
            for j in colunas_de_interesse:
                if j!='dt_inclusao':
                    d[j]=dados.loc[i, lista_colunas_de_interesse][colunas_de_interesse[j]]                
                # print(j+': ', dados.loc[i, lista_colunas_de_interesse][colunas_de_interesse[j]])        

                    #         info=dt_obj.strftime("%d-%m-%y")
            if d['tipo_contratacao']=='PESSOA FÍSICA':
                if d['cpf']=='NaN':
                    senha=d['cnpj']
                else:
                    senha=d['cpf']
                    from datetime import datetime
                    d['data_nascimento'] = datetime.strptime(str(d['data_nascimento']), '%d/%m/%Y')

                form=Form_Usuario(d)
                if form.is_valid():
                    user = User.objects.create_user(
                        username=d['email'], 
                        email=d['email'], 
                        password=senha
                        )
                    user.first_name = d['nome']
                    user.set_password(senha)
                    user.save()
                    usuario = form.save()
                    usuario.user = user
                    usuario.save()
                    cont_usuarios_cadastrados+=1
                    
                    valores=d['area'].split(';')
                    
                    ids=[]
                    for u in valores:   
                        # print(u)          
                        area=u.strip()    
                        # print(area)      
                        try:                       
                            ids.append(Area_Atuacao.objects.get(area=area).id)
                        except:
                            ids.append('')
                            error_area.append([d['cpf'], valores, area])
                    
                    d['area']=ids
                    
                    form2=Form_Artista(d)
                    if form2.is_valid():
                        obj=form2.save()
                        obj.tipo_contratacao = TiposContratação.objects.get(id=1)
                        obj.user_responsavel = user
                        form2.save()
                        cont_artista+=1
                        
                    else:
                        print('Indice: '+str(i))
                        print('Nome: '+str(d['nome']))
                        print('CPF: '+str(d['cpf']))
                        print('Telefone: '+str(d['telefone']))
                        print('Erro no formulário do artista:')                    
                        print(form2.errors)
                        print('''-------------------------------------------------------------------------''')
                        cont_erro_artista+=1                    
                else:
                    print('Indice: '+str(i))
                    print('Nome: '+str(d['nome']))
                    print('CPF: '+str(d['cpf']))
                    print('Telefone: '+str(d['telefone']))
                    print('Erro no formulário do usuário:')                
                    print(form.errors)
                    print('''-------------------------------------------------------------------------''')
                    cont_erro_user+=1
                cont_fisica+=1            
            else:
                cont+=1
                            
    print('Erros ao cadastrar usuários: ',cont_erro_user)        
    print('PJ: ',cont)
    print('PF: ',cont_fisica)
    print('Artistas: ',cont_artista)
    print('Erros ao cadastrar artista: ',cont_erro_artista)        
    print('Áreas que não conseguiu cadastrar: ', error_area)    
    context={
        # 'print': df_.loc[:, area_atuacao].to_html,
        'print': dados.to_html
    }
    return render(request, 'auxiliar.html', context)


@login_required
def indicadores(request):

    context = {
        'vagas': 0,
        'balcao': 0,
        'online': 0,
        'balcao2': 0,
        'online2': 0,
        'buscar': 0
    }

    return render(request, 'indicadores.html', context)
