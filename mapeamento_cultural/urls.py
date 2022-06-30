from django.contrib import admin
from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.index),
    
    path('cadastrar-se', views.cadastro_usuario, name='cadastrar_usuario'),

    path('mapeamento-cultural/', views.mapeamento_cultural, name='mapeamento'),
    path('mapeamento-cultural/lei-866-93-art-25', views.lei866, name='lei866'),
    path('mapeamento-cultural/cadastrar', views.cadastro_etapa_1, name='cad_cult_etapa1'),
    path('mapeamento-cultural/cadastrar/artista', views.cadastro_etapa_1_artista, name='cad_cult_etapa1_artista'),
    path('mapeamento-cultural/get_form_cpf', views.get_form_cpf, name='get_form_cpf'),
    path('mapeamento-cultural/get_form_cnpj', views.get_form_cnpj, name='get_form_cpf'),
]
