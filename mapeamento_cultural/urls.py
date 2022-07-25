from django.contrib import admin
from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.index),
    path('login/', views.login_view),
    path('logout/', views.logout),
    
    path('cadastrar-se', views.cadastro_usuario, name='cadastrar_usuario'),
    
    path('adm/cadastros', views.admin_cadastros, name='admin_cadastros'),
    path('acc/meu-perfil', views.meu_perfil, name='acc_meu_perfil'),
    path('acc/meu-perfil/mudar-senha', views.change_password, name='acc_mudar_senha'),
    path('acc/meus_cadastros', views.meus_cadastros, name='acc_meus_cadastros'),
    path('acc/meus_cadastros/detalhes/', views.cadastro_map_cultural_cpf, name='acc_meus_cadastros_map'),
    path('acc/meus_cadastros/detalhes/editar/b', views.editar_artista_b, name='acc_editar_map_b'),
    path('acc/meus_cadastros/detalhes/editar/c', views.editar_artista_c, name='acc_editar_map_c'),
    path('acc/meus_cadastros/detalhes/editar/cmp', views.editar_etapa_2, name='acc_editar_map_cmp'),    
    #path('acc/meus_cadastros/detalhes/02<id>', views.cadastro_map_cultural_cnpj, name='acc_meus_cadastros_map_cnpj'),
    
    path('mapeamento-cultural/', views.mapeamento_cultural, name='mapeamento'),
    path('mapeamento-cultural/lei-866-93-art-25', views.lei866, name='lei866'),
    path('mapeamento-cultural/cadastrar', views.cadastro_etapa_1, name='cad_cult_etapa1'),
    path('mapeamento-cultural/cadastrar/fazedor-de-cultura', views.cadastro_etapa_1_artista, name='cad_cult_etapa1_artista'),
    path('mapeamento-cultural/cadastrar/prestador-de-servico-cultural', views.cadastro_etapa_1_empresa, name='cad_cult_etapa1_empresa'),
    path('mapeamento-cultural/cadastrar/etapa-2/', views.cadastro_etapa_2, name='cad_cult_etapa2'),    
    path('mapeamento-cultural/get_form_cpf', views.get_form_cpf, name='get_form_cpf'),
    path('mapeamento-cultural/get_form_cnpj', views.get_form_cnpj, name='get_form_cpf'),

    path('mapeamento-cultural/cadastrar/etapa-3/', views.cadastro_etapa_3, name='cad_cult_etapa3'),
    path('mapeamento-cultural/cadastrar/anexos/', views.cadastro_anexo, name='cad_cult_anexo'),

    # path('teste/', views.qr_code)
]
