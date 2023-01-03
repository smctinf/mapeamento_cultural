from django.contrib import admin
from django.urls import path
from . import views
 
urlpatterns = [
    path('editais/', views.editais, name='editais'),
    path('editais/cultura-planeja', views.editais, name='editais1'),
    path('editais/credenciamento-parecerista', views.editais2, name='editais2'),
]