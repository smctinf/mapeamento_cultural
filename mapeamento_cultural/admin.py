from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(TiposContratação)
admin.site.register(ArtistaContratoCPF)
admin.site.register(ArtistaContratoCNPJ)
admin.site.register(Area_Atuacao)
admin.site.register(Publico_Atuacao)
admin.site.register(Enquadramento_Atuacao)
admin.site.register(Forma_insercao_Atuacao)
admin.site.register(InformacoesExtras)