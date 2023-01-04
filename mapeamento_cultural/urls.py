from django.contrib import admin
from django.urls import path
from . import views
 
urlpatterns = [
    
    path('', views.index),    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('cadastrar-se', views.cadastro_usuario, name='cadastrar_usuario'),
    
    path('adm/cadastros', views.admin_cadastros, name='admin_cadastros'),
    path('acc/meu-perfil', views.meu_perfil, name='acc_meu_perfil'),
    path('acc/meu-perfil/mudar-senha', views.change_password, name='acc_mudar_senha'),
    path('acc/meu-perfil/alterar-dados-pessoais', views.alterar_meus_dados, name='acc_alterar_meus_dados'),
    path('acc/meus_cadastros/', views.meus_cadastros, name='acc_meus_cadastros'),
    path('acc/meus_cadastros/1d1d61<id>d9281', views.cadastro_map_cultural_cpf, name='acc_meus_cadastros_map'),
    path('acc/meus_cadastros/1d1d61<id>d9281/editar/b/', views.editar_artista_b, name='acc_editar_map_b'),
    path('acc/meus_cadastros/1d1d61<id>d9281/editar/c/', views.editar_artista_c, name='acc_editar_map_c'),
    path('acc/meus_cadastros/1d61<id>d9281/editar/cmp/', views.editar_etapa_2, name='acc_editar_map_cmp'),    
    path('acc/meus_cadastros/1d61<id>d9281/anexos/', views.cadastro_anexo, name='cad_cult_anexo'),
    path('acc/meus_cadastros/1d61<id>d9281/anexos/deletar-recibo/', views.deletar_anexo, name='deletar_recibo'),
    path('acc/meus_cadastros/1d1d61<id>d9281/excluir', views.excluir_map_cultural, name='acc_meus_cadastros_map_excluir'),
    #path('acc/meus_cadastros/detalhes/02<id>', views.cadastro_map_cultural_cnpj, name='acc_meus_cadastros_map_cnpj'),
    
    path('mapeamento-cultural/', views.mapeamento_cultural, name='mapeamento'),
    path('mapeamento-cultural/listagem', views.mapeamento_listagem, name='mapeamento_listagem'),
    path('mapeamento-cultural/lei-866-93-art-25', views.lei866, name='lei866'),    
    path('mapeamento-cultural/cadastrar/', views.cadastro_etapa_1, name='cad_cult_etapa1_artista'),
    path('mapeamento-cultural/cadastrar/cpf/', views.cadastro_cpf, name='cad_artista_cpf'),
    path('mapeamento-cultural/cadastrar/cnpj/', views.cadastro_cnpj, name='cad_artista_cnpj'),    
    #path('mapeamento-cultural/cadastrar/prestador-de-servico-cultural', views.cadastro_etapa_1_empresa, name='cad_cult_etapa1_empresa'),
    path('mapeamento-cultural/cadastrar/etapa-2/<id>', views.cadastro_etapa_2, name='cad_cult_etapa2'),    

    #GETS p/ cadastro_inicial.html
    path('mapeamento-cultural/get_form_cpf', views.get_form_cpf, name='get_form_cpf'),
    path('mapeamento-cultural/get_form_cnpj', views.get_form_cnpj, name='get_form_cpf'),

    path('mapeamento-cultural/cadastrar/etapa-3/<id>', views.cadastro_etapa_3, name='cad_cult_etapa3'),
    
    path('email', views.enviar_email)
    # path('teste/', views.qr_code)
]
