from django import template
from ..models import InformacoesExtras
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def descricao(obj):       
    try:
        info = InformacoesExtras.objects.get(id_artista=obj.id)
        return info.descricao
    except:
        return mark_safe('Não há descrição cadastrada.')

@register.filter
def area_atuacao(obj):       
    areas=obj.area.all()
    texto=''
    for i in areas:
        texto+=str(i)+'<br><br>'
    
        
    return mark_safe(texto)